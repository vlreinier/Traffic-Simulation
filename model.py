from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import CarAgent
from random import random, randint, choice


class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, road_length):
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.lanes = lanes
        self.road_length = road_length
        self.car_id = 0
        self.space_between_cars = 3
        self.starting_point = 0
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)
        self.speed_colors = {1: "#B41A0B", 2: "#1C8B08"}
        self.car_frequency = 0.2  # 50% per step

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        for lane in range(self.lanes):
            if self.space_available(lane) and (random() < self.car_frequency):
                max_car_speed = 1
                color = self.speed_colors[max_car_speed]
                car = CarAgent(self.car_id, self, max_car_speed, color)
                self.schedule.add(car)
                self.grid.place_agent(agent=car, pos=(self.starting_point, lane))
                self.car_id += 1

    def space_available(self, lane):
        for cell in range(self.starting_point, self.space_between_cars + 1):
            if not self.grid.is_cell_empty((cell, lane)):
                return False
        return True

