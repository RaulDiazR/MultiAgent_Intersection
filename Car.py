import numpy as np
from mesa import Agent, Model

matrix = [
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [1,1,1,1,1,1,5,3,1,2,2,2,2,1,5,3,1,1,1,1,1,1],
    [6,6,6,6,6,6,7,3,1,2,2,2,2,1,5,8,6,6,6,6,6,6],
    [4,4,4,4,4,4,7,3,1,2,2,2,2,1,5,8,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,3,1,2,2,2,2,1,5,3,1,1,1,1,1,1],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,3,1,2,2,2,2,1,5,3,1,2,2,2,2,2],
    [1,1,1,1,1,1,5,3,1,1,1,1,1,1,5,3,1,1,1,1,1,1],
    [6,6,6,6,6,6,9,9,6,6,6,6,6,6,9,9,6,6,6,6,6,6],
    [4,4,4,4,4,4,9,9,4,4,4,4,4,4,9,9,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,3,1,1,1,1,1,1,5,3,1,1,1,1,1,1],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,3,1,2,2,2,2,1,5,3,1,3,3,3,3,3]
    ]

# AJUSTAR VARIABLES DE CONTROL PARA PERMITIR Y ANALIZAR MOVIMIENTOS EN NEGATIVO
  
class Car(Agent):
  def __init__(self, model: Model, pos, speed):
    super().__init__(model.next_id(), model)
    self.pos = pos
    self.speed = speed
    # orientations for traffic lights and cars
    # 0 -> south
    # 1 -> east
    # 2 -> north
    # 3 -> west
    if speed[0] != 0.0:
      self.axis = 0 
      self.orientation = 1 if self.speed[0] > 0.0 else 3
    else:
      self.axis = 1
      self.orientation = 0 if self.speed[1] > 0.0 else 2
    
    self.traffic_light = self.find_nearest_traffic_light()
    self.check_TL = False

  def step(self):
    car_ahead = self.car_ahead()
    #print("SPEED:", self.speed)
    
    if self.check_TL: 
      self.traffic_light = self.find_nearest_traffic_light()

    if car_ahead == None:
      traffic_light_ahead = self.traffic_light_ahead()
      if traffic_light_ahead != False:
        new_speed = self.brake(traffic_light_ahead) 
      else:
        new_speed = self.accelerate() 
    else:
      new_speed = self.decelerate(car_ahead)
      
    if new_speed >= 1.0:
      new_speed = 1.0
    elif new_speed <= 0.0:
      new_speed = 0.0

    self.speed = np.array([0.0, 0.0])
    self.speed[self.axis] = new_speed
    
    new_pos = self.pos + np.array([0.3, 0.3]) * self.speed
    self.model.space.move_agent(self, new_pos)

  def car_ahead(self):
    for neighbor in self.model.space.get_neighbors(self.pos, 1.0):
      if neighbor.pos[self.axis] > self.pos[self.axis] and type(neighbor) == Car:
        return neighbor
    return None

  def accelerate(self):
    return self.speed[self.axis] + 0.05

  def decelerate(self, car_ahead):
    return car_ahead.speed[self.axis] - 0.1
    
  def brake(self, deceleration):    
    # Calculate the required reduction in speed
    #print("Car ID:", self.unique_id, "Speed:" ,self.speed[self.axis], "Orientation:", self.axis)
    return self.speed[self.axis] - deceleration

  
  def traffic_light_ahead(self):
    axis = self.axis
    distance = (self.traffic_light.pos[axis]) - self.pos[axis]
    #print("DISTANCE TO CHANGE TFS",distance)
    #print(self.traffic_light.pos)
    if distance > 0.0:
      self.check_TL = False
      if (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance < 4.0 and distance > 0.15:
        # only decelerate the following amount 
        return 0.05 if self.speed[self.axis] > 0.5 else 0.0
      elif (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance < 0.3 and distance > 0.0:
        return 1.0
    else:
      self.check_TL = True
    
    return False
    
  def find_nearest_traffic_light(self):
    min_distance = 100
    nearest_traffic_light = None
    
    for traffic_light in self.model.traffic_lights:
      if self.orientation == traffic_light.orientation:
        i = 0 if self.axis == 1 else 1
        distance = self.calculate_distance(self.pos, traffic_light.pos)
        
        # axisDifference represents the distance between the axis opposite to the car's movement, so it can choose 
        # the correct traffic light based on the fact that the traffic light corresponding to each car should not 
        # be further than 1.5 of diantce in said axis
        axisDifference = abs(traffic_light.pos[i] - self.pos[i])
        if distance < min_distance and distance > 0.0 and axisDifference < 1.5:
            min_distance = distance
            nearest_traffic_light = traffic_light
    #print("CHOOSE TF",distance)
            
    return nearest_traffic_light
            
  def calculate_distance(self,car_pos, traffic_light_pos):
    car_x, car_y = car_pos
    light_x, light_y = traffic_light_pos
    distance = ((car_x - light_x) ** 2 + (car_y - light_y) ** 2) ** 0.5
    return distance

    
