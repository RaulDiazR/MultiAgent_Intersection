import numpy as np
from mesa import Agent, Model

class Car(Agent):
  def __init__(self, model: Model, pos, speed):
    super().__init__(model.next_id(), model)
    self.pos = pos
    self.speed = speed
    self.orientation = 0 if speed[0] != 0.0 else 1

  def step(self):
    car_ahead = self.car_ahead()
    #print(traffic_light.pos[0], traffic_light.pos[1])
    self.traffic_light = self.find_nearest_traffic_light()
    check_TL = False
    
    if check_TL: self.traffic_light = self.find_nearest_traffic_light()

    if car_ahead == None:
      traffic_light_ahead = self.traffic_light_ahead()
      if traffic_light_ahead:
        new_speed = self.brake(traffic_light_ahead) 
      else:
        new_speed = self.accelerate() 
    else:
      new_speed = self.decelerate(car_ahead)
      
    if new_speed >= 1.0:
      new_speed = 1.0
    elif new_speed <= 0.0:
      new_speed = 0.0

    self.speed = np.array([new_speed, 0.0])
    new_pos = self.pos + np.array([0.3, 0.0]) * self.speed
    self.model.space.move_agent(self, new_pos)

  def car_ahead(self):
    for neighbor in self.model.space.get_neighbors(self.pos, 1):
      if neighbor.pos[0] > self.pos[0] and type(neighbor) == Car:
        return neighbor
    return None

  def accelerate(self):
    return self.speed[0] + 0.05

  def decelerate(self, car_ahead):
    return car_ahead.speed[0] - 0.1
    
  def brake(self, deceleration):    
    # Calculate the required reduction in speed
    #print("Car ID:", self.unique_id, "Speed:" ,self.speed[self.orientation], "Orientation:", self.orientation)
    return self.speed[0] - deceleration

  
  def traffic_light_ahead(self):
    # if self.traffic_light.state == 1 or self.traffic_light.state == 2:
    #   i = self.traffic_light.orientation 
    #   distance = (self.traffic_light.pos[i] - 2) - self.pos[i]
    #   min_braking_distance = 3.0
      
    #   if distance < min_braking_distance and distance > 0.0:
    #     return distance if distance > 1.0 else 1.0
    i = self.traffic_light.orientation 
    distance = (self.traffic_light.pos[i] - 3) - self.pos[i]
    print(self.traffic_light.pos[i] - 3)
    if distance > 0.0:
      if (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance < 4.0 and distance > 0.15:
        # only decelerate the following amount 
        return 0.05 if self.speed[self.orientation] > 0.5 else 0.0
      
      elif (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance < 0.15 and distance > 0.0:
        return 1.0
    
    return False
    
  def find_nearest_traffic_light(self):
    min_distance = 100
    nearest_traffic_light = None
    
    for traffic_light in self.model.traffic_lights:
      if self.orientation == traffic_light.orientation:
        distance = self.calculate_distance(self.pos, traffic_light.pos)
        if distance < min_distance:
            min_distance = distance
            nearest_traffic_light = traffic_light
            
    return nearest_traffic_light
            
  def calculate_distance(self,car_pos, traffic_light_pos):
    car_x, car_y = car_pos
    light_x, light_y = traffic_light_pos
    distance = ((car_x - light_x) ** 2 + (car_y - light_y) ** 2) ** 0.5
    return distance

    
