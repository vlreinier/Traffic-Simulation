from mesa import Agent

class Vehicle(Agent):
    def __init__(self, unique_id, model, max_vehicle_speed, color, type):
        """Constructor for car agent"""
        super(Vehicle, self).__init__(unique_id, model)
        self.max_vehicle_speed = max_vehicle_speed
        self.color = color
        self.last_overtake = 0
        self.type = type

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
        if self.model.road_length <= self.pos[0] + self.model.space_between_vehicles + 1:
            return False
        elif space > 0 and space > self.max_vehicle_speed:
            return self.max_vehicle_speed
        elif space > 0:
            return space
        else:
            return 0

    def move_vehicle(self):
        #// Move up or down if possible
        spacer = int(self.model.space_between_vehicles / 2)
        space_in_front = self.space_in_front()
        if space_in_front < self.max_vehicle_speed:
            space_below, locations_below = self.space_below(spacer)
            space_above, locations_above = self.space_above(spacer)

            if space_below and space_above and (self.type == "Truck" or self.type == "Car") and self.pos[1] != 0:
                self.move_down(space_below, locations_below)
            elif space_below and space_above and self.type == "Bike":
                self.last_overtake += 1
                if (self.last_overtake == 0 or space_in_front == 0) and self.pos[1] < self.model.lanes-1:
                    self.move_up(space_above, locations_above)
            elif space_above and not space_below and self.pos[1] < self.model.lanes-1 and self.pos[0]-spacer > 0:
                self.move_up(space_above, locations_above)
            elif space_below and not space_above and self.pos[1] != 0:
                self.move_down(space_below, locations_below)

        if self.last_overtake == 4:
            self.last_overtake = 0

        #// Move forward if possible
        available_space = self.get_available_space()
        if not available_space:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.model.grid.move_agent(self, (self.pos[0] + available_space, self.pos[1]))

    def space_above(self, spacer):
        switch_locations = []
        switch_lane = True
        for cell in range(self.pos[0] - spacer - 1, self.pos[0] + spacer + 1):
            if not self.model.grid.is_cell_empty((cell, self.pos[1] + 1)):
                switch_lane = False
            switch_locations.append((cell, self.pos[1] + 1))
        return switch_lane, switch_locations

    def space_below(self, spacer):
        switch_locations = []
        switch_lane = True
        for cell in range(self.pos[0] - spacer - 1, self.pos[0] + spacer + 1):
            if not self.model.grid.is_cell_empty((cell, self.pos[1] - 1)):
                switch_lane = False
            switch_locations.append((cell, self.pos[1] - 1))
        return switch_lane, switch_locations

    def move_up(self, switch_lane, switch_locations):
        if switch_lane and len(switch_locations) > 0:
            self.model.grid.move_agent(self, (switch_locations[int(len(switch_locations) / 2)]))

    def move_down(self, switch_lane, switch_locations):
        if switch_lane and len(switch_locations) > 0:
            self.model.grid.move_agent(self, (switch_locations[int(len(switch_locations) / 2)]))


class Obstacle(Agent):
    """Constructor for obstacle agent"""
    def __init__(self, unique_id, model):
        super(Obstacle, self).__init__(unique_id, model)
