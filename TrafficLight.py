import numpy as np
from mesa import Agent, Model
class TrafficLight(Agent):
  def __init__(self, model: Model, position, orientation):
    super().__init__(model.next_id(), model)
    # orientations for traffic lights and cars
    # 0 -> south
    # 1 -> east
    # 2 -> north
    # 3 -> west
    self.orientation = orientation
    # sets the default duration in seconds of the traffic light
    self.duration = 200
    
    # Changes traffic light time according to orientation so they are coordinated   
    if self.orientation == "SOUTH" or self.orientation == "NORTH":
      self.gTime = self.duration * 0.4
      self.rTime = self.duration * 0.5
    else:
      self.gTime = self.duration * 0.3
      self.rTime = self.duration * 0.6
      
    self.yTime = self.duration*0.1

    # stores durations for the green, yellow and red lights
    self.counts = [self.gTime, self.yTime, self.rTime]
    
    # states:
    # 0 -> Green
    # 1 -> Yellow
    # 2 -> Red
    self.state = 0 if self.orientation == "SOUTH" or self.orientation == "NORTH" else 2
    
    # stores position in space
    self.pos = position

  def step(self):
    state = self.state
    
    if self.counts[state] == 0:
      if state == 0:
        self.counts[state] = self.gTime
      elif state == 2:
        self.counts[state] = self.rTime
      else:
        self.counts[state] = self.yTime
        
      self.state = self.state + 1 if self.state < 2 else 0
    
    
    self.counts[state] -= 1
    #print(self.state)

