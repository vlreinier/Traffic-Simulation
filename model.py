from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import CarAgent, Obstacle
from random import random, randint


class Road(Model):
    def __init__(self, lanes, road_length, car_frequency, space_between_cars, obstacles = [(40, 0),(45, 1)]):
        """Constructor for model"""
        self.schedule = SimultaneousActivation(self)
        self.lanes = lanes
        self.road_length = road_length
        self.car_frequency = car_frequency
        self.space_between_cars = space_between_cars
        self.obstacles = obstacles
        self.running = True
        self.car_id = 0
        self.obstacle_id = 0
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)
        self.speed_colors = {1: "#3F9D3E", 2: "#28716D", 3: "#482871", 4:"#71284E", 5:"#000000"}
        self.obstacle_color = '#FF0000'
        self.place_obstacles()

    def place_obstacles(self):
        """Place obstacles on grid"""
        for i in self.obstacles:
            if not i[1] in list(range(self.lanes)): continue
            self.grid.place_agent(agent=Obstacle(self, self.obstacle_id, self.obstacle_color), pos=(i[0], i[1]))
            self.obstacle_id += 1

    def choose_lane(self, speed):
        """Cars choose a lane by their speed"""
        if speed <= int(len(self.speed_colors) / 2) and random() < 0.80:  # 80% chance slow cars start on right lanes
            return randint(0, int(self.lanes / 2))
        if speed >= int(len(self.speed_colors) / 2) and random() < 0.80:  # 80% chance fast cars start on left lanes
            return randint(int(self.lanes / 2), self.lanes - 1)
        else:
            return randint(0, self.lanes - 1)

    def lane_space(self, lane):
        """Calculates if space in lane for starting cars"""
        for cell in range(0, self.space_between_cars):
            if not self.grid.is_cell_empty((cell, lane)):
                return False
        return True

    def step(self):
        """Step function for simultaneous activation agents"""
        self.schedule.step()
        for lane in range(self.lanes):
            if random() < self.car_frequency:
                speed = randint(min(self.speed_colors), len(self.speed_colors))
                lane = self.choose_lane(speed)
                if self.lane_space(lane):
                    car = CarAgent(self.car_id, self, speed, self.speed_colors[speed])
                    self.schedule.add(car)
                    self.grid.place_agent(agent=car, pos=(0, lane))
                    self.car_id += 1
