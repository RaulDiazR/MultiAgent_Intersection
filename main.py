import numpy as np
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
from auxFiles.SimpleContinuousModule import SimpleCanvas
import random

from Car import Car
from TrafficLight import TrafficLight

class Street(Agent):
  def __init__(self, model, orientation):
    super().__init__(model.next_id(), model)
    
  def step(self):
    return
    
class City(Model):
  
  def __init__(self):
    super().__init__()
    self.space = ContinuousSpace(22, 22, True)
    self.schedule = RandomActivation(self)
    self.matrix = [
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [1,1,1,1,1,1,5,7,1,1,1,1,1,1,5,7,1,1,1,1,1,1],
    [6,6,6,6,6,6,8,10,6,6,6,6,6,6,8,10,6,6,6,6,6,6],
    [4,4,4,4,4,4,9,11,4,4,4,4,4,4,9,11,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,7,1,2,2,2,2,1,5,7,1,1,1,1,1,1],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [2,2,2,2,2,1,5,7,1,2,2,2,2,1,5,7,1,2,2,2,2,2],
    [1,1,1,1,1,1,5,7,1,2,2,2,2,1,5,7,1,1,1,1,1,1],
    [6,6,6,6,6,6,8,7,1,2,2,2,2,1,5,7,6,6,6,6,6,6],
    [4,4,4,4,4,4,9,7,1,2,2,2,2,1,5,11,4,4,4,4,4,4],
    [1,1,1,1,1,1,5,7,1,2,2,2,2,1,5,7,1,1,1,1,1,1],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3],
    [3,3,3,3,3,1,5,7,1,2,2,2,2,1,5,7,1,3,3,3,3,3]
    ]
    
    
    self.traffic_lights = [] # Almacena los semáforos para revisarlos en la clase carros
    
    self.drawStreets()
    self.drawTrafficLights()
    self.drawCars()
      
  def step(self):
    self.schedule.step()
    
  def drawCars(self):
    # --- Horizontal Cars ---
    
    # West Cars
    py = 6
    px = 20
    for i in range(0):
      px += i
      car = Car(self, np.array([px, py]),)
      self.space.place_agent(car, car.pos)
      self.schedule.add(car)
      
    # East Cars
    py = 7
    for px in range(1):
      car = Car(self, np.array([px, py]),)
      self.space.place_agent(car, car.pos)
      self.schedule.add(car)

    # --- Vertical Cars ---
    
    # South Cars
    first = True
    for py in range(0):
      if first:
        px = 6
        first = False
      else:
        px = 14
        first = True
      py += 1
      car = Car(self, np.array([px, py]),)
      self.space.place_agent(car, car.pos)
      self.schedule.add(car)
      
    # North Cars
    first = True
    for py in range(0):
      if first:
        px = 7
        first = False
      else:
        px = 15
        first = True
      py += 1
      car = Car(self, np.array([px, py]),)
      self.space.place_agent(car, car.pos)
      self.schedule.add(car)
    
  def drawTrafficLights(self):
    traffic_lights_coords_east = [
      np.array([13, 8]),
      np.array([5, 8]),
      np.array([5, 16]),
    ]
    
    traffic_lights_coords_west = [
      np.array([16, 5]),
      np.array([8, 5]),
      np.array([16, 13]),
    ]
      
    traffic_lights_coords_south = [
      np.array([13, 5]),
      np.array([5, 5]),
      np.array([5, 13]),
      np.array([13, 13]),
    ]
    traffic_lights_coords_north = [
      np.array([16, 8]),
      np.array([8, 8]),
      np.array([16, 16]),
      np.array([8, 16]),
    ]
    
    # orientations for traffic lights and cars
    # 0 -> south
    # 1 -> east
    # 2 -> north
    # 3 -> west
    
    for tf_coord in traffic_lights_coords_west:      
      traffic_light = TrafficLight(self, tf_coord, "WEST")
      self.space.place_agent(traffic_light, traffic_light.pos)
      self.schedule.add(traffic_light)
      self.traffic_lights.append(traffic_light)
    
    for tf_coord in traffic_lights_coords_north:      
      traffic_light = TrafficLight(self, tf_coord, "NORTH")
      self.space.place_agent(traffic_light, traffic_light.pos)
      self.schedule.add(traffic_light)
      self.traffic_lights.append(traffic_light)

    for tf_coord in traffic_lights_coords_east:      
      traffic_light = TrafficLight(self, tf_coord, "EAST")
      self.space.place_agent(traffic_light, traffic_light.pos)
      self.schedule.add(traffic_light)
      self.traffic_lights.append(traffic_light)
      
    for tf_coord in traffic_lights_coords_south:      
      traffic_light = TrafficLight(self, tf_coord, "SOUTH")
      self.space.place_agent(traffic_light, traffic_light.pos)
      self.schedule.add(traffic_light)
      self.traffic_lights.append(traffic_light)
    
  def drawStreets(self):
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix)):
        if self.matrix[i][j] >= 4:
          street = Street(self, 0)
          self.space.place_agent(street,(j, i))
          self.schedule.add(street)
   
      
def agent_draw(agent):
  if type(agent) == Car:
    color = "Blue" if agent.unique_id % 2 == 0 else "Purple"
    if agent.axis == 0:
      return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}
    else:
      return {"Shape": "rect", "w": 0.02, "h": 0.034, "Filled": "true", "Color": color}

  elif type(agent) == TrafficLight:
    if agent.state == 0:
      color = "Green"
    elif agent.state == 1:
      color = "Yellow"
    elif agent.state == 2:
      color = "Red"
    if agent.orientation == "EAST" or agent.orientation == "WEST":
      return {"Shape": "rect", "w": 0.015, "h": 0.04, "Filled": "true", "Color": color}
    else:
      return {"Shape": "rect", "w": 0.04, "h": 0.015, "Filled": "true", "Color": color}
  
  elif type(agent) == Street:
    return {"Shape": "rect", "w": 0.1, "h": 0.1, "Filled": "false", "Color": "Gray"}
    

canvas = SimpleCanvas(agent_draw, 500, 500)


model_params = {}

server = ModularServer(City, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
