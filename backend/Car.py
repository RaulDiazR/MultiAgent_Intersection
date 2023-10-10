import numpy as np
from mesa import Agent, Model
import math
import random

# AJUSTAR VARIABLES DE CONTROL PARA PERMITIR Y ANALIZAR MOVIMIENTOS EN NEGATIVO


class Car(Agent):
    def __init__(self, model: Model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos  # current position
        self.orientation = ""
        self.matrix = model.matrix
        newCell = self.matrix[math.floor(self.pos[1])][math.floor(self.pos[0])]
        orientation = self.decideDirection(newCell)
        self.orientate(orientation)
        self.cell = newCell
        self.turn = ""

        self.traffic_light = self.findNearestTrafficLight()
        self.check_TL = False  # support variable that indicates if a new traffic light has to be found (happens when the car gets ahead of its current traffic light)

    def step(self):
        carAhead = self.carAhead()  # check if theres any car ahead
        currCell = self.matrix[math.floor(self.pos[1])][math.floor(self.pos[0])]
        if self.pos[self.axis] >= 22: self.pos[self.axis] -= 1
        if self.checkTurn(currCell, self.pos[0], self.pos[1]) and self.turn != "": #check if it needs to turn
            self.orientate(self.turn)
            self.orientation = self.turn
            self.cell = currCell
            self.turn = ""
        else: #Check if there will be a turn in the future
            stepsAhead = 2
            futurePos0 = self.pos[0]+self.speed[0]*stepsAhead
            futurePos1 = self.pos[1]+self.speed[1]*stepsAhead
            if not self.model.space.out_of_bounds((futurePos0, futurePos1)):
                aheadCell = self.matrix[math.floor(futurePos1)][math.floor(futurePos0)]
                if self.checkTurn(aheadCell, futurePos0, futurePos1):
                    turnDirection = self.decideDirection(aheadCell)
                    self.turn = turnDirection if turnDirection != self.orientation else ""


        if self.check_TL:
            self.traffic_light = self.findNearestTrafficLight()
        # if there is no car ahead, it checks if the nearest traffic light is close
        if carAhead == None:
            braking_speed = self.traffic_light_ahead()
            if braking_speed:
                new_speed = self.brake(braking_speed)
            else:
                new_speed = self.accelerate()

        # decelerates if there is a car ahead
        else:
            new_speed = self.decelerate(carAhead)

        speedLimit = 0.25

        if self.movementDir == 1:
            if new_speed >= speedLimit:
                new_speed = speedLimit
            elif new_speed <= 0.0:
                new_speed = 0.0
        else:
            if new_speed <= -speedLimit:
                new_speed = -speedLimit
            elif new_speed >= 0.0:
                new_speed = 0.0

        self.speed = np.array([0.0, 0.0])
        self.speed[self.axis] = new_speed
        
        new_pos = self.pos + self.speed
        self.model.space.move_agent(self, new_pos)

    def carAhead(self):
        # checks if there is a car ahead, in said case it decelerates so it doesn´t crash
        radius = 1 if self.movementDir == 1 else 2
        for neighbor in self.model.space.get_neighbors(self.pos, radius, False):
            if (
                self.movementDir == 1
                and neighbor.pos[self.axis] > self.pos[self.axis]
                and type(neighbor) == Car
                and self.orientation == neighbor.orientation
            ):
                return neighbor

            elif (
                self.movementDir == -1
                and self.pos[self.axis] > neighbor.pos[self.axis]
                and type(neighbor) == Car
                and self.orientation == neighbor.orientation
            ):
                return neighbor
        return None

    def checkTurn(self, currCell, pos0, pos1):
        offset = 0.3
        return (
            pos0 + offset < len(self.matrix)
            and pos1 + offset < len(self.matrix)
            and pos0 - offset > 0
            and pos1 - offset > 0
            and currCell
            == self.matrix[math.floor(pos1 + offset)][math.floor(pos0 + offset)]
            and currCell
            == self.matrix[math.floor(pos1 - offset)][math.floor(pos0 - offset)]
        ) and currCell != self.cell


    def accelerate(self):
        return self.speed[self.axis] + (0.01 * self.movementDir)

    def decelerate(self, carAhead):
        return carAhead.speed[self.axis] - (0.05 * self.movementDir)

    def brake(self, deceleration):
        # brakes the given amount, which can be either small or big enough to stop the car completely
        return self.speed[self.axis] - deceleration

    def traffic_light_ahead(self):
        if self.traffic_light == None:
            return False  # a contingency so the program doesn't crash in rare scenarios
        axis = self.axis
        distance = (self.traffic_light.pos[axis]) - self.pos[
            axis
        ]  # distance between the car and the its traffic light
        # checks if there is a red or yellow light nearby the car
        if self.movementDir == 1:
            if (
                distance > 0.0
            ):  # checks if the car has not gotten ahead of the traffic light
                self.check_TL = False
                if (
                    (self.traffic_light.state == 1 or self.traffic_light.state == 2)
                    and distance < 4.0
                    and distance > 0.4
                ):
                    # if theres a yellow or red light close only decelerates the following amount
                    return 0.01 if self.speed[self.axis] > 0.1 else 0.0
                elif (
                    (self.traffic_light.state == 1 or self.traffic_light.state == 2)
                    and distance < 0.4
                    and distance > 0.0
                ):
                    # stops completely if the traffic light is in front of the car
                    return 1.0
            else:
                # if the car has passed the traffic light, it searches for the next traffic light in its path
                self.check_TL = True

        # same as the previous process, but it is modified for negative movement
        else:
            if distance < 0.0:
                self.check_TL = False
                if (
                    (self.traffic_light.state == 1 or self.traffic_light.state == 2)
                    and distance > -4.0
                    and distance < -0.4
                ):
                    return -0.01 if self.speed[self.axis] < -0.1 else 0.0
                elif (
                    (self.traffic_light.state == 1 or self.traffic_light.state == 2)
                    and distance > -0.4
                    and distance < 0.0
                ):
                    return -1.0
            else:
                self.check_TL = True

        return False

    def findNearestTrafficLight(self):
        min_distance = 100  # support variable to get the min distance
        nearest_traffic_light = None

        for traffic_light in self.model.traffic_lights:
            if self.orientation == traffic_light.orientation:
                i = (
                    0 if self.axis == 1 else 1
                )  # support variable to see the axisDifference
                distance = self.calculateDistance(self.pos, traffic_light.pos)

                # axisDifference represents the distance between the axis opposite to the car's movement, so it can choose
                # the correct traffic light based on the fact that the traffic light corresponding to each car should not
                # be further than 1.5 of diantce in said axis
                axisDifference = abs(traffic_light.pos[i] - self.pos[i])
                if distance < min_distance and distance > 0.0 and axisDifference < 5.0:
                    min_distance = distance
                    nearest_traffic_light = traffic_light

        return nearest_traffic_light

    def calculateDistance(self, car_pos, traffic_light_pos):
        # Calculates the euclidan distance between a car and a traffic light
        car_x, car_y = car_pos
        light_x, light_y = traffic_light_pos
        distance = ((car_x - light_x) ** 2 + (car_y - light_y) ** 2) ** 0.5
        return distance

    def decideDirection(self, newCell):
        # Decide orientation based on type of cell
        if newCell == 4:
            orientation = "EAST"
        elif newCell == 5:
            orientation = "SOUTH"
        elif newCell == 6:
            orientation = "WEST"
        elif newCell == 7:
            orientation = "NORTH"
        elif newCell == 8:
            if self.cell == 6:
              orientation = "WEST"
            else:  
              orientation = self.randomDirection("WEST", "SOUTH")
        elif newCell == 9:
            if self.cell == 5:
                orientation = "SOUTH"
            else:
                orientation = self.randomDirection("SOUTH", "EAST")
        elif newCell == 10:
            if self.cell == 7:
                orientation = "NORTH"
            else:
                orientation = self.randomDirection("NORTH", "WEST")
        elif newCell == 11:
            if self.cell == 4:
                orientation = "EAST"
            else:
                orientation = self.randomDirection("NORTH", "EAST")
        else:
            orientation = "NORTH"
        return orientation
        

    def randomDirection(self, direction1, direction2):
        prob = random.random()
        if prob < 0.5:
            return direction1
        else:
            return direction2

    def orientate(self, newOrientation):
        # orientations for traffic lights and cars
        if newOrientation == self.orientation:
            return
        self.orientation = newOrientation
        if self.orientation == "NORTH":
            self.axis = 1
            self.speed = np.array([0, -0.1])
        elif self.orientation == "SOUTH":
            self.axis = 1
            self.speed = np.array([0, 0.1])
        elif self.orientation == "EAST":
            self.axis = 0
            self.speed = np.array([0.1, 0])
        else:
            self.axis = 0
            self.speed = np.array([-0.1, 0])
        # movement direction for cars based on grid values (0,0 of grid is located at the upper-left corner)
        # south: positive movement
        # east: positive movement
        # north: negative movement
        # west: negative movement
        self.movementDir = (
            1 if self.orientation == "SOUTH" or self.orientation == "EAST" else -1
        )
