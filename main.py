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
    self.orientation = orientation
    
  def step(self):
    return
    
class City(Model):
  
  def __init__(self):
    super().__init__()
    self.space = ContinuousSpace(22, 22, True)
    self.schedule = RandomActivation(self)
    
    self.traffic_lights = []
    
    self.drawStreets()
    
    first = True
    py = 7
    px = 0
    for _ in np.random.choice(22 + 1, 5, replace=False):
      px +=1
      if first:
        car = Car(self, np.array([px, py]), np.array([1.0, 0.0]))
        first = False
      else:
        car = Car(self, np.array([px, py]), np.array([self.random.randrange(2, 7, 2)/10, 0.0]))
      self.space.place_agent(car, car.pos)
      self.schedule.add(car)
      
    traffic_lights_coords_horizontal = [
      np.array([16, 5]),
      np.array([8, 5]),
      
      np.array([13, 8]),
      np.array([5, 8]),
    ]
      
    traffic_lights_coords_vertical = [
      np.array([13, 5]),
      np.array([5, 5]),
      
      np.array([16, 8]),
      np.array([8, 8]),
    ]
    
    for tf_coord in traffic_lights_coords_horizontal:      
      traffic_light = TrafficLight(self, 24, tf_coord, 0)
      self.space.place_agent(traffic_light, traffic_light.pos)
      self.schedule.add(traffic_light)
      self.traffic_lights.append(traffic_light)
      
    for tf_coord in traffic_lights_coords_vertical:      
      traffic_light = TrafficLight(self, 24, tf_coord, 1)
      self.space.place_agent(traffic_light, traffic_light.pos)
      self.schedule.add(traffic_light)
      self.traffic_lights.append(traffic_light)
    
    
      
  def step(self):
    self.schedule.step()
    
  def drawStreets(self):
    for i in range(22):
      street = Street(self, 0)
      self.space.place_agent(street, np.array([i, 6]))
      self.schedule.add(street)
      street = Street(self, 0)
      self.space.place_agent(street, np.array([i, 7]))
      self.schedule.add(street)
      
    for i in range(22):
      street = Street(self, 1)
      self.space.place_agent(street, np.array([6, i]))
      self.schedule.add(street)
      street = Street(self, 1)
      self.space.place_agent(street, np.array([7, i]))
      self.schedule.add(street)
      
    for i in range(22):
      street = Street(self, 1)
      self.space.place_agent(street, np.array([14, i]))
      self.schedule.add(street)
      street = Street(self, 1)
      self.space.place_agent(street, np.array([15, i]))
      self.schedule.add(street)
      
    for i in range(8):
      street = Street(self, 0)
      self.space.place_agent(street, np.array([i, 14]))
      self.schedule.add(street)
      street = Street(self, 0)
      self.space.place_agent(street, np.array([i, 15]))
      self.schedule.add(street)
      
    for i in range(8):
      i += 14
      street = Street(self, 0)
      self.space.place_agent(street, np.array([i, 14]))
      self.schedule.add(street)
      street = Street(self, 0)
      self.space.place_agent(street, np.array([i, 15]))
      self.schedule.add(street)
      
def car_draw(agent):
  if type(agent) == Car:
    color = "Blue" if agent.unique_id % 2 == 0 else "Purple"
    return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}
  
  elif type(agent) == TrafficLight:
    if agent.state == 0:
      color = "Green"
    elif agent.state == 1:
      color = "Yellow"
    elif agent.state == 2:
      color = "Red"
    if agent.orientation == 0:
      return {"Shape": "rect", "w": 0.015, "h": 0.04, "Filled": "true", "Color": color}
    else:
      return {"Shape": "rect", "w": 0.04, "h": 0.015, "Filled": "true", "Color": color}
  
  elif type(agent) == Street:
    if agent.orientation == 0:
      return {"Shape": "rect", "w": 0.05, "h": 0.034, "Filled": "false", "Color": "Gray"}
    else:
      return {"Shape": "rect", "w": 0.034, "h": 0.05, "Filled": "false", "Color": "Gray"}
    

canvas = SimpleCanvas(car_draw, 500, 500)


model_params = {}

server = ModularServer(City, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
