from mesa import Agent
from random import random, choice, randint


class Vehicle(Agent):
    def __init__(self, unique_id, model, max_vehicle_speed, color, type):
        """Constructor for car agent"""
        super(Vehicle, self).__init__(unique_id, model)
        self.max_vehicle_speed = max_vehicle_speed
        self.color = color
        self.last_overtake = 0
        self.min_overtake = randint(4,6)
        self.type = type
        self.last_move = 0

    def advance(self):
        self.move_vehicle()

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

    def move_vehicle(self):
        #// Move up or down if possible
        spacer = int(self.model.space_between_vehicles / 2) + 1
        space_in_front = self.get_available_space()

        #// Check if there is any space to move
        if self.pos[1] != 0:
            space_below, location_below = self.space_below(spacer)
        else:
            space_below, location_below = False, False
        if self.pos[1]+1 < self.model.lanes-1:
            space_above, location_above = self.space_above(spacer)
        else:
            space_above, location_above = False, False

        #// If statements to determine vehicle behaviour
        if (space_in_front < self.max_vehicle_speed) and space_below and space_above:
            self.last_overtake += 1
            choice([self.move_down(space_below, location_below),self.move_up(space_above, location_above)])
        elif (space_in_front < self.max_vehicle_speed) and space_below and not space_above:
            self.last_overtake += 1
            self.move_down(space_below, location_below)
        elif (space_in_front < self.max_vehicle_speed) and not space_below and space_above:
            self.last_overtake += 1
            self.move_up(space_below, location_below)
        elif (space_in_front < self.max_vehicle_speed) and space_above and self.last_overtake == 0:
            self.last_overtake += 1
            self.move_up(space_above, location_above)
        elif space_below:
            self.last_overtake += 1
            self.move_down(space_below, location_below)

        if self.last_overtake == self.min_overtake:
            self.last_overtake = 0

        #// Move forward if possible
        available_space = self.get_available_space()
        if self.model.road_length <= self.pos[0] + self.model.space_between_vehicles + 1:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.model.grid.move_agent(self, (self.pos[0] + available_space, self.pos[1]))

    def space_above(self, spacer):
        switch_locations = []
        switch_lane = True
        for cell in range(self.pos[0] - spacer, self.pos[0] + spacer):
            if not self.model.grid.is_cell_empty((cell, self.pos[1] + 1)):
                switch_lane = False
            switch_locations.append((cell, self.pos[1] + 1))
        return switch_lane, switch_locations[int(len(switch_locations) / 2)]

    def space_below(self, spacer):
        switch_locations = []
        switch_lane = True
        for cell in range(self.pos[0] - spacer, self.pos[0] + spacer):
            if not self.model.grid.is_cell_empty((cell, self.pos[1] - 1)):
                switch_lane = False
            switch_locations.append((cell, self.pos[1] - 1))
        return switch_lane, switch_locations[int(len(switch_locations) / 2)]

    def move_up(self, switch_lane, switch_location):
        if switch_lane:
            self.model.grid.move_agent(self, switch_location)

    def move_down(self, switch_lane, switch_location):
        if switch_lane:
            self.model.grid.move_agent(self, switch_location)


class Obstacle(Agent):
    """Constructor for obstacle agent"""
    def __init__(self, unique_id, model):
        super(Obstacle, self).__init__(unique_id, model)
