import numpy as np
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
from auxFiles.SimpleContinuousModule import SimpleCanvas
import random
 
from Car import Car
from TrafficLight import TrafficLight

class Dummy(Agent):
  def __init__(self, model):
    super().__init__(model.next_id(), model)
    
  def step(self):
    return
    
class Street(Model):
  
  def __init__(self):
    super().__init__()
    self.space = ContinuousSpace(22, 22, True)
    self.schedule = RandomActivation(self)
    
    self.traffic_lights = []
    
    dummy = Dummy(self)
    self.space.place_agent(dummy, np.array([15, 6]))
    self.schedule.add(dummy)
    dummy = Dummy(self)
    self.space.place_agent(dummy, np.array([14, 6]))
    self.schedule.add(dummy)
    
    
    first = True
    py = 6
    px = 0
    for _ in np.random.choice(6 + 1, 5, replace=False):
      px +=1
      if first:
        car = Car(self, np.array([px, py]), np.array([1.0, 0.0]))
        first = False
      else:
        car = Car(self, np.array([px, py]), np.array([self.random.randrange(2, 7, 2)/10, 0.0]))
      self.space.place_agent(car, car.pos)
      self.schedule.add(car)
      
    traffic_light = TrafficLight(self, 54, np.array([16, 7]), 0)
    self.space.place_agent(traffic_light, traffic_light.pos)
    self.schedule.add(traffic_light)
    self.traffic_lights.append(traffic_light)
  
    
      
  def step(self):
    self.schedule.step()
      
def car_draw(agent):
  if type(agent) == Car:
    #color = "Blue" if agent.unique_id % 2 == 0 else "Purple"
    if agent.unique_id == 3:
      color = "Blue"
    elif agent.unique_id == 4:
      color = "Purple"
    elif agent.unique_id == 5:
      color = "Black"
    elif agent.unique_id == 6:
      color = "Red"
    elif agent.unique_id == 7:
      color = "Green"
    return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}
  
  elif type(agent) == TrafficLight:
    if agent.state == 0:
      color = "Green"
    elif agent.state == 1:
      color = "Yellow"
    elif agent.state == 2:
      color = "Red"
    return {"Shape": "rect", "w": 0.02, "h": 0.034, "Filled": "true", "Color": color}
  
  elif type(agent) == Dummy:
    return {"Shape": "rect", "w": 0.02, "h": 0.034, "Filled": "false", "Color": "Gray"}
    

canvas = SimpleCanvas(car_draw, 500, 500)


model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
