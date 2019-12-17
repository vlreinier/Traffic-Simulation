from mesa import Agent
from random import random, choice, randint


class Vehicle(Agent):
    def __init__(self, unique_id, model, max_vehicle_speed, type):
        """Constructor for car agent"""
        super(Vehicle, self).__init__(unique_id, model)
        self.max_vehicle_speed = max_vehicle_speed
        self.unique_id = unique_id
        self.type = type
        self.space_upfront = 0
        self.speed = 0
        self.last_switch = 0
        self.spacer = int(self.model.space_between_vehicles / 2) + 1

    def advance(self):
        """Required function for Agent class. Is run every step in model"""
        #  first calculate new space in front of agent
        self.space_upfront = self.get_space_upfront(self.pos[0], self.pos[1])

        #  if switch lane returns not False but a tuple with location:
        switch_lane = self.lane_switch()
        if type(switch_lane) == tuple:
            self.last_switch = 0
            self.move_vehicle(switch_lane)
        else:
            self.lane_forward()

    def lane_forward(self):
        """If possible move available space forward"""
        #  if end of road remove agent
        if self.model.road_length <= self.pos[0] + self.model.space_between_vehicles + 1:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:  # move forward
            self.last_switch += 1
            self.move_vehicle((self.pos[0] + self.space_upfront, self.pos[1]))

    def lane_switch(self):
        """Determine if car can and must switch lane, and if so return location"""
        # First check if spaces below and above are empty
        space_below, location_below = False, False
        space_above, location_above = False, False
        if self.pos[1] != 0:  # if lane is not bottom lane
            space_below, location_below = self.space_on_side(self.spacer, -1)
        if self.pos[1] < self.model.lanes - 1:  # if lane is not top lane
            space_above, location_above = self.space_on_side(self.spacer, 1)

        # If statements to determine if car will switch lane
        if self.space_upfront < self.max_vehicle_speed and self.last_switch > 4:
            if space_below and space_above:
                if self.get_preferred_lane() == 0 and (int(self.model.max_type_speed / 2) > self.max_vehicle_speed):
                    return location_above
                return location_below
            if space_below:
                return location_below
            if space_above:
                return location_above
        elif space_below and self.get_space_upfront(self.pos[0], self.pos[1] - 1) >= self.max_vehicle_speed:
            return location_below

        return False

    def get_space_upfront(self, x, y):
        """Get space up front for x (cell) and y (lane) coordinates of position"""
        space = -self.model.space_between_vehicles
        for i in range(1, self.model.road_length - x):
            if self.model.grid.is_cell_empty((x + i, y)):
                space += 1
                if space >= self.max_vehicle_speed:
                    break
            else:
                break
        if space > 0:
            return space
        return 0

    def get_preferred_lane(self):
        """Get preferred lane"""
        # get space in lane above and below
        space_above = self.get_space_upfront(self.pos[0], self.pos[1] + 1)
        space_below = self.get_space_upfront(self.pos[0], self.pos[1] - 1)
        # prefer lane above
        if space_below > space_above:
            return 0
        else:
            return 1

    def space_on_side(self, spacer, lane):
        """Check if space on side is available and if so, return location in the midst"""
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

    def move_vehicle(self, next_position):
        """Move vehicle to another position on grid"""
        if self.model.grid.is_cell_empty(next_position):
            self.speed = next_position[0] - self.pos[0]
            self.model.grid.move_agent(self, next_position)


class Obstacle(Agent):
    """Constructor for obstacle agent"""

    def __init__(self, unique_id, model, type):
        super(Obstacle, self).__init__(unique_id, model)
        self.type = type
