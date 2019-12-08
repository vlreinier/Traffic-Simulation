from mesa import Agent
from random import random, choice, randint

class Vehicle(Agent):
    def __init__(self, unique_id, model, max_vehicle_speed, color, type):
        """Constructor for car agent"""
        super(Vehicle, self).__init__(unique_id, model)
        self.max_vehicle_speed = max_vehicle_speed
        self.color = color
        self.type = type
        self.last_move = 0

    def space_in_front(self):
        space = 0
        for i in range(1, self.model.road_length - self.pos[0]):  # remaining cells until end road
            if self.model.grid.is_cell_empty((self.pos[0] + i, self.pos[1])):
                space += 1
            else:
                break
        return space - self.model.space_between_vehicles

    def get_available_space(self):
        space = self.space_in_front()
        if space > 0 and space > self.max_vehicle_speed:
            return self.max_vehicle_speed
        elif space > 0:
            return space
        else:
            return 0

    def space_neighbour_lane(self, spacer, lane):
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
        #// Move up or down if possible
        # Get space in front and spacer for changing lanes
        space_in_front = self.get_available_space()
        spacer = int(self.model.space_between_vehicles / 2)

        #// Check if there is any space to move up or down
        if self.pos[1] != 0:  # if lane is not bottom lane
            space_below, location_below = self.space_neighbour_lane(spacer, -1)
        else:
            space_below, location_below = False, False
        if self.pos[1] < self.model.lanes -1:  # if lane is not top lane
            space_above, location_above = self.space_neighbour_lane(spacer, 1)
        else:
            space_above, location_above = False, False

        # // If statements to determine vehicle behaviour
        switch_lane = False
        if (space_in_front < self.max_vehicle_speed) and self.last_move == 0:
            if space_above and self.type in ['Bike', 'Car'] and random() < 0.5:
                switch_lane = location_above
            elif space_above and not space_below and self.type in ['Truck']:
                switch_lane = location_above
            elif space_below:
                switch_lane = location_below
        elif self.type == "Truck" and self.last_move == 0 and space_below:
            switch_lane = location_below
        self.last_move += 1
        if self.last_move == 7:
            self.last_move = 0

        #// Else move forward
        if switch_lane:
            self.move_vehicle(switch_lane)
        else:
            if self.model.road_length <= self.pos[0] + self.model.space_between_vehicles + 1:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
            else:
                self.move_vehicle((self.pos[0] + space_in_front, self.pos[1]))


class Obstacle(Agent):
    """Constructor for obstacle agent"""
    def __init__(self, unique_id, model):
        super(Obstacle, self).__init__(unique_id, model)
