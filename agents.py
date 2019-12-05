from mesa import Agent


class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, max_car_speed, color):
        super(CarAgent, self).__init__(unique_id, model)
        self.max_car_speed = max_car_speed
        self.color = color
        self.switching_lanes = False
        self.available_space = 0

    def advance(self):
        self.switch_lane()
        self.move_forward()

    def switch_lane(self):
        spacer = int(self.model.space_between_cars / 2)
        switch_locations = []
        switch_lane = True
        if self.space_in_front() < self.max_car_speed and self.pos[1] < self.model.lanes-1 and self.pos[0]-spacer > 0:
            for cell in range(self.pos[0] - spacer - 1, self.pos[0] + spacer + 1):
                if not self.model.grid.is_cell_empty((cell, self.pos[1] + 1)):
                    switch_lane = False
                switch_locations.append((cell, self.pos[1] + 1))
            if switch_lane and len(switch_locations) > 0:
                self.model.grid.move_agent(self, (switch_locations[int(len(switch_locations) / 2)]))

    def move_forward(self):
        if self.model.road_length <= self.pos[0] + self.model.space_between_cars + 1:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.available_space = self.get_available_space()
            self.model.grid.move_agent(self, (self.pos[0] + self.available_space, self.pos[1]))

    def space_in_front(self):
        space = 0
        for i in range(1, self.model.road_length - self.pos[0]):
            if self.model.grid.is_cell_empty((self.pos[0] + i, self.pos[1])):
                space += 1
            else:
                break
        return space - self.model.space_between_cars

    def get_available_space(self):
        space = self.space_in_front()
        if space > 0 and space > self.max_car_speed:
            return self.max_car_speed
        elif space > 0:
            return space
        else:
            return 0


class Obstacle(Agent):
    def __init__(self, unique_id, model, color):
        super(Obstacle, self).__init__(unique_id, model)
        self.color = color
