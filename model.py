from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import CarAgent
from random import random, randint


class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, road_length, car_frequency):
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.lanes = lanes
        self.road_length = road_length
        self.car_id = 0
        self.space_between_cars = 3
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)
        self.speed_colors = {1: "#FF1700", 2: "#C27910", 3: "#2EC210"}
        self.car_frequency = car_frequency / 100
        self.first_run = [True] * self.lanes

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        for lane in range(self.lanes):
            if self.space_available(lane) and (random() < self.car_frequency):
                max_car_speed = randint(1, len(self.speed_colors))
                color = self.speed_colors[max_car_speed]
                car = CarAgent(self.car_id, self, max_car_speed, color, first_run=self.first_run[lane])
                self.schedule.add(car)
                self.grid.place_agent(agent=car, pos=(0, lane))
                self.car_id += 1
                self.first_run[lane] = False

    def space_available(self, lane):
        for cell in range(0, self.space_between_cars):
            if not self.grid.is_cell_empty((cell, lane)):
                return False
        return True

