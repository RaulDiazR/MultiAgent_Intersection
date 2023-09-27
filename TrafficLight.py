import numpy as np
from mesa import Agent, Model
auxTL = 2
class TrafficLight(Agent):
  def __init__(self, model: Model, duration, position, orientation):
    super().__init__(model.next_id(), model)
    # 0 -> X axis
    # 0 -> Y axis
    self.orientation = orientation
    # sets the default duration in seconds of the traffic light
    self.duration = duration
    # stores durations for the green, yellow and red lights
    self.counts = [duration, duration//auxTL, duration]
    
    # states:
    # 0 -> Green
    # 1 -> Yellow
    # 2 -> Red
    self.state = 0
    
    # stores position in space
    self.pos = position

  def step(self):
    state = self.state
    
    if self.counts[state] == 0:
      if state == 0 or state == 2:
        self.counts[state] = self.duration
        
      else:
        self.counts[state] = self.duration//auxTL
        
      self.state = self.state + 1 if self.state < 2 else 0
    
    
    self.counts[state] -= 1
    #print(self.state)

