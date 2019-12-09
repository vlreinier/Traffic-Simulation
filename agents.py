from mesa import Agent
from random import random, choice, randint
from math import floor

class Vehicle(Agent):
    def __init__(self, unique_id, model, max_vehicle_speed, type):
        """Constructor for car agent"""
        super(Vehicle, self).__init__(unique_id, model)
        self.max_vehicle_speed = max_vehicle_speed
        self.type = type
        self.same_lane = 0
        self.last_acceleration = 0
        self.unique_id = unique_id

    def advance(self):
        space_in_front = self.space_in_front()
        space_on_front_and_back = floor(self.model.space_between_vehicles / 2)
        switch_lane = self.lane_switch(space_on_front_and_back, space_in_front)
        self.lane_forward(switch_lane, space_in_front)

    def lane_forward(self, switch_lane, space_in_front):
        if switch_lane:
            self.last_acceleration = 0
            self.same_lane = 0
            self.move_vehicle(switch_lane)
        if self.model.road_length <= self.pos[0] + self.model.space_between_vehicles + 1:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return
        self.last_acceleration = space_in_front
        self.same_lane += 1
        if self.same_lane == 3: self.same_lane = 0
        self.move_vehicle((self.pos[0] + space_in_front, self.pos[1]))

    def lane_switch(self, switch_space, space_in_front):
        # # 'pseudo' code to work out:
        # if int(self.model.max_type_speed / 2) >= self.max_vehicle_speed:
        #     direction = probably_down or stay_in_lane
        # if int(self.model.max_type_speed / 2) < self.max_vehicle_speed:
        #     direction = probably_up or stay_in_lane
        space_below, location_below = False, False
        space_above, location_above = False, False

        if self.pos[1] != 0:  # if lane is not bottom lane
            space_below, location_below = self.space_on_side(switch_space, -1)
        if self.pos[1] < self.model.lanes - 1:  # if lane is not top lane
            space_above, location_above = self.space_on_side(switch_space, 1)

        # // If statements to determine vehicle behaviour
        if space_in_front < self.max_vehicle_speed and space_below and space_above and self.same_lane == 0:
            if self.get_best_lane_switch() == 0 and (floor(self.model.max_type_speed / 2) > self.max_vehicle_speed):
                return location_above
            return location_below
        elif space_in_front < self.max_vehicle_speed and space_below and self.same_lane == 0:
            return location_below
        elif space_in_front < self.max_vehicle_speed  and space_above and self.same_lane == 0:
            return location_above
        elif self.space_up_front(self.pos[0], self.pos[1] - 1) >= self.max_vehicle_speed and \
                space_below and self.same_lane == 0:
            return location_below
        return False

    def space_in_front(self):
        return self.space_up_front(self.pos[0], self.pos[1])

    def space_up_front(self, x, y):
        space = -self.model.space_between_vehicles
        for i in range(1, self.model.road_length - x):  # remaining cells until end road
            if self.model.grid.is_cell_empty((x + i, y)):
                space += 1
                if space >= self.max_vehicle_speed:
                    break
            else:
                break
        if space > 0:
            return space
        return 0

    def get_best_lane_switch(self):
        space_above = self.space_up_front(self.pos[0], self.pos[1] + 1)
        space_below = self.space_up_front(self.pos[0], self.pos[1] - 1)

        # prefer lane above
        if space_below > space_above:
            return 0
        else:
            return 1


    def space_on_side(self, spacer, lane):
        switch_locations = []
        switch_lane = True
        max_x = (
            self.pos[0] + spacer 
            if self.pos[0] + spacer < self.model.road_length 
            else self.model.road_length 
        )
        for cell in range(self.pos[0] - spacer, max_x):
            if not self.model.grid.is_cell_empty((cell, self.pos[1] + lane)):
                switch_lane = False
            switch_locations.append((cell, self.pos[1] + lane))
        return switch_lane, switch_locations[int(len(switch_locations) / 2)]

    def move_vehicle(self, switch_location):
        if self.model.grid.is_cell_empty(switch_location):
            self.model.grid.move_agent(self, switch_location)


class Obstacle(Agent):
    """Constructor for obstacle agent"""
    def __init__(self, unique_id, model, type):
        super(Obstacle, self).__init__(unique_id, model)
        self.type = type
