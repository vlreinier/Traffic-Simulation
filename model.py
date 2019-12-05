from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import CarAgent, Obstacle
from random import random, randint


class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, road_length, car_frequency, space_between_cars, obstacles = [(45, 0),(40, 0)]):
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.lanes = lanes
        self.road_length = road_length
        self.car_id = 0
        self.obstacle_id = 0
        self.space_between_cars = space_between_cars
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)
        self.speed_colors = {1: "#CB21AC", 2: "#2EC210", 3: "#2133CB", 4:"#30CB21", 5:"#000000"}
        self.car_frequency = car_frequency / 100
        self.first_run = [True] * self.lanes
        self.obstacles = obstacles
        self.obstacle_color = '#808080'

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        for i in range(self.lanes):
            speed = randint(min(self.speed_colors), len(self.speed_colors))
            lane = self.choose_lane(speed)
            if self.space_available(lane) and (random() < self.car_frequency):
                color = self.speed_colors[speed]
                car = CarAgent(self.car_id, self, speed, color, first_run=self.first_run[lane])
                self.schedule.add(car)
                self.grid.place_agent(agent=car, pos=(0, lane))
                self.car_id += 1
                self.first_run[lane] = False
        self.place_obstacles()

    def place_obstacles(self):
        if len(self.obstacles) > 0:
            for i in self.obstacles:
                obstacle = Obstacle(self, self.obstacle_id, self.obstacle_color)
                self.grid.place_agent(agent=obstacle, pos=(i[0], i[1]))
                self.obstacle_id += 1

    def choose_lane(self, speed):
        if speed <= int(len(self.speed_colors) / 2) and random() < 0.90:
            return randint(0, int(self.lanes / 2))
        if speed >= int(len(self.speed_colors) / 2) and random() < 0.90:
            return randint(int(self.lanes / 2), self.lanes - 1)
        else:
            return randint(0, self.lanes - 1)

    def space_available(self, lane):
        for cell in range(0, self.space_between_cars):
            if not self.grid.is_cell_empty((cell, lane)):
                return False
        return True
