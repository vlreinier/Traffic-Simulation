from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import CarAgent
from random import getrandbits


class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, road_length):
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.lanes = lanes
        self.road_length = road_length
        self.car_id = 0
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        for lane in range(self.lanes):
            if getrandbits(1):
                car_length = 5
                car_speed = 1
                car = CarAgent(self.car_id, self, car_length, car_speed)
                self.schedule.add(car)
                self.grid.place_agent(car, (0, lane))
                #self.place_car(lane, car, car_length)
                self.car_id += 1


    def place_car(self, lane, car, cells):
        for cell in range(cells):
            self.grid.place_agent(car, (cell, lane))
