from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import Vehicle, Obstacle
from random import random, randint, choice
import numpy as np


class Road(Model):
    def __init__(self, lanes, road_length, vehicle_frequency, space_between_vehicles, obstacle_lane):
        """Constructor for the Road, the model for this agent-based simulation, 'housing' the agents,
        and setting up and configuring the simulation"""
        self.schedule = SimultaneousActivation(self)
        self.lanes = lanes
        self.road_length = road_length
        self.vehicle_frequency = vehicle_frequency
        self.space_between_vehicles = space_between_vehicles
        self.obstacle_lane = obstacle_lane
        self.running = True
        self.types = {'🚗': [1, (1, 1)]}
        self.max_type_speed = max([speed for type in self.types for speed in self.types[type][1]])
        self.vehicle_id = 0
        self.obstacle_id = 0
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)
        self.place_obstacles()

    def place_obstacles(self):
        """Places given number of random obstacles on grid"""
        if self.obstacle_lane != 'nulmeting':
            self.grid.place_agent(agent=Obstacle(self, self.obstacle_id, type=choice(['⚠️','⛔'])),
                                  pos=(int(self.road_length / 2), self.obstacle_lane))
            self.obstacle_id += 1

    def choose_lane(self, speed):
        """Cars choose a lane by their speed"""
        if speed <= int(len(self.types) / 2):
            return randint(0, int(self.lanes / 2))
        elif speed > int(len(self.types) / 2):
            return randint(int(self.lanes / 2), self.lanes - 1)
        else:
            return randint(0, self.lanes - 1)

    def lane_space(self, lane):
        """Calculates if space in lane for starting cars"""
        for cell in range(0, self.space_between_vehicles):
            if not self.grid.is_cell_empty(pos=(cell, lane)):
                return False
        return True

    def pick_random_traffic_type(self, type_dict):
        """Picks traffic type from dictionary where each type has its own chance of appearance"""
        types = []
        probabilities = []
        for type, info in type_dict.items():
            types.append(type)
            probabilities.append(info[0])
        return np.random.choice(types, 1, p=probabilities)[0]

    def step(self):
        """Step function for simultaneous activation agents"""
        self.schedule.step()
        for lane in range(self.lanes):
            if random() < self.vehicle_frequency:
                type = self.pick_random_traffic_type(self.types)
                speed = randint(self.types[type][1][0], self.types[type][1][1])
                lane = self.choose_lane(speed=speed)
                if self.lane_space(lane=lane):
                    vehicle = Vehicle(self.vehicle_id, self, speed, type)
                    self.schedule.add(vehicle)
                    self.grid.place_agent(agent=vehicle, pos=(0, lane))
                    self.vehicle_id += 1
