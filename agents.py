from mesa import Agent
from random import random, choice, randint


class Vehicle(Agent):
    def __init__(self, unique_id, model, max_vehicle_speed, type):
        """Constructor for car agent"""
        super(Vehicle, self).__init__(unique_id, model)
        self.max_vehicle_speed = max_vehicle_speed
        self.type = type
        self.same_lane = 0
        self.switch_space = int(self.model.space_between_vehicles / 2) + 1
        self.last_acceleration = 0

    def space_in_front(self):
        space = 0
        for i in range(1, self.model.road_length - self.pos[0]):  # remaining cells until end road
            if self.model.grid.is_cell_empty((self.pos[0] + i, self.pos[1])):
                space += 1
            else:
                break
        space = space - self.model.space_between_vehicles
        if space > 0 and space > self.max_vehicle_speed:
            return self.max_vehicle_speed
        elif space > 0:
            return space
        else:
            return 0

    def space_on_side(self, spacer, lane):
        switch_locations = []
        switch_lane = True
        for cell in range(self.pos[0] - spacer, self.pos[0] + spacer):
            if not self.model.grid.is_cell_empty((cell, self.pos[1] + lane)):
                switch_lane = False
            switch_locations.append((cell, self.pos[1] + lane))
        return switch_lane, switch_locations[int(len(switch_locations) / 2)]

    def move_vehicle(self, switch_location):
        self.model.grid.move_agent(self, switch_location)

    def advance(self):
        if self.pos[1] != 0:  # if lane is not bottom lane
            space_below, location_below = self.space_on_side(self.switch_space, -1)
        else:
            space_below, location_below = False, False
        if self.pos[1] < self.model.lanes -1:  # if lane is not top lane
            space_above, location_above = self.space_on_side(self.switch_space, 1)
        else:
            space_above, location_above = False, False

        # // If statements to determine vehicle behaviour
        switch_lane = False
        space_in_front = self.space_in_front()

        if space_in_front == 0 and space_below and self.last_acceleration == 0 and self.same_lane == 1:
            switch_lane = location_below
        elif space_in_front == 0 and space_above and self.last_acceleration == 0 and self.same_lane == 1:
            switch_lane = location_above
        elif space_in_front < self.max_vehicle_speed and self.same_lane == 5 and space_above:
            switch_lane = location_above
        elif space_below and space_in_front == self.max_vehicle_speed and self.same_lane == 5:
            switch_lane = location_below

        if switch_lane:
            self.last_acceleration = 0
            self.same_lane = 0
            self.move_vehicle(switch_lane)
        else:
            if self.model.road_length <= self.pos[0] + self.model.space_between_vehicles + 1:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                self.last_acceleration = space_in_front
                self.same_lane += 1
                self.move_vehicle((self.pos[0] + space_in_front, self.pos[1]))

class Obstacle(Agent):
    """Constructor for obstacle agent"""
    def __init__(self, unique_id, model, type):
        super(Obstacle, self).__init__(unique_id, model)
        self.type = type
