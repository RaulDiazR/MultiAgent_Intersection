import numpy as np
from mesa import Agent, Model

# AJUSTAR VARIABLES DE CONTROL PARA PERMITIR Y ANALIZAR MOVIMIENTOS EN NEGATIVO
  
class Car(Agent):
  def __init__(self, model: Model, pos, speed):
    super().__init__(model.next_id(), model)
    self.pos = pos # current position
    self.speed = speed # current speed
    self.matrix = model.matrix 
    
    # orientations for traffic lights and cars
    # 0 -> south: positive movement
    # 1 -> east: positive movement
    # 2 -> north: negative movement
    # 3 -> west: negative movement 
    if speed[0] != 0.0:
      self.axis = 0 
      self.orientation = 1 if self.speed[0] > 0.0 else 3
    else:
      self.axis = 1
      self.orientation = 0 if self.speed[1] > 0.0 else 2
    
    # movement direction for cars based on grid values (0,0 of grid is located at the upper-left corner)
    # south: positive movement
    # east: positive movement
    # north: negative movement
    # west: negative movement 
    self.movementDir = 1 if self.orientation == 0 or self.orientation == 1 else -1
    
    self.traffic_light = self.find_nearest_traffic_light()
    self.check_TL = False # support variable that indicates if a new traffic light has to be found (happens when the car gets ahead of its current traffic light)

  def step(self):
    car_ahead = self.car_ahead() # check if theres any car ahead 
    
    if self.check_TL: 
      self.traffic_light = self.find_nearest_traffic_light()

    # if there is no car ahead, it checks if the nearest traffic light is close
    if car_ahead == None:
      braking_speed = self.traffic_light_ahead()
      if braking_speed != False:
        new_speed = self.brake(braking_speed) 
      else:
        new_speed = self.accelerate() 
        
    # decelerates if there is a car ahead
    else:
      new_speed = self.decelerate(car_ahead)
      
    if self.movementDir == 1:
      if new_speed >= 1.0:
        new_speed = 1.0
      elif new_speed <= 0.0:
        new_speed = 0.0
    else:
      if new_speed <= -1.0:
        new_speed = -1.0
      elif new_speed >= 0.0:
        new_speed = 0.0

    self.speed = np.array([0.0, 0.0])
    self.speed[self.axis] = new_speed
    
    new_pos = self.pos + np.array([0.3, 0.3]) * self.speed
    self.model.space.move_agent(self, new_pos)

  def car_ahead(self):
    # checks if there is a car ahead, in said case it decelerates so it doesn´t crash
    radius = 0.5 if self.movementDir == 1 else 1.5
    for neighbor in self.model.space.get_neighbors(self.pos, radius, False):
      if self.movementDir == 1 and neighbor.pos[self.axis] > self.pos[self.axis] and type(neighbor) == Car and self.orientation == neighbor.orientation:
        return neighbor
      
      elif self.movementDir == -1 and self.pos[self.axis] > neighbor.pos[self.axis] and type(neighbor) == Car and self.orientation == neighbor.orientation:
        return neighbor
    return None

  def accelerate(self):
    return self.speed[self.axis] + (0.05*self.movementDir)

  def decelerate(self, car_ahead):
    return car_ahead.speed[self.axis] - (0.1*self.movementDir)
    
  def brake(self, deceleration):    
    # brakes the given amount, which can be either small or big enough to stop the car completely
    return self.speed[self.axis] - deceleration
  
  def traffic_light_ahead(self):
    if self.traffic_light == None: return False # a contingency so the program doesn't crash in rare scenarios
    axis = self.axis
    distance = (self.traffic_light.pos[axis]) - self.pos[axis] # distance between the car and the its traffic light
    # checks if there is a red or yellow light nearby the car
    if self.movementDir == 1:
      if distance > 0.0: # checks if the car has not gotten ahead of the traffic light
        self.check_TL = False
        if (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance < 4.0 and distance > 0.4:
          # if theres a yellow or red light close only decelerates the following amount 
          return 0.05 if self.speed[self.axis] > 0.5 else 0.0
        elif (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance < 0.4 and distance > 0.0:
          # stops completely if the traffic light is in front of the car
          return 1.0
      else:
        # if the car has passed the traffic light, it searches for the next traffic light in its path
        self.check_TL = True
        
    # same as the previous process, but it is modified for negative movement
    else:
      if distance < 0.0:
        self.check_TL = False
        if (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance > -4.0 and distance < -0.4:
          return -0.05 if self.speed[self.axis] < -0.5 else 0.0
        elif (self.traffic_light.state == 1 or self.traffic_light.state == 2) and distance > -0.4 and distance < 0.0:
          return -1.0
      else:
        self.check_TL = True
    
    return False
    
  def find_nearest_traffic_light(self):
    min_distance = 100 # support variable to get the min distance
    nearest_traffic_light = None
    
    for traffic_light in self.model.traffic_lights:
      if self.orientation == traffic_light.orientation:
        i = 0 if self.axis == 1 else 1 # support variable to see the axisDifference
        distance = self.calculate_distance(self.pos, traffic_light.pos)
        
        # axisDifference represents the distance between the axis opposite to the car's movement, so it can choose 
        # the correct traffic light based on the fact that the traffic light corresponding to each car should not 
        # be further than 1.5 of diantce in said axis
        axisDifference = abs(traffic_light.pos[i] - self.pos[i])
        if distance < min_distance and distance > 0.0 and axisDifference < 1.5:
            min_distance = distance
            nearest_traffic_light = traffic_light
            
    return nearest_traffic_light
            
  def calculate_distance(self,car_pos, traffic_light_pos):
    # Calculates the euclidan distance between a car and a traffic light
    car_x, car_y = car_pos
    light_x, light_y = traffic_light_pos
    distance = ((car_x - light_x) ** 2 + (car_y - light_y) ** 2) ** 0.5
    return distance

    
