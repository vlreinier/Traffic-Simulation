from mesa import Agent


class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, max_car_speed, color, first_run):
        super(CarAgent, self).__init__(unique_id, model)
        self.max_car_speed = max_car_speed
        self.color = color
        self.first_run = first_run
        self.switching_lanes = False
        self.available_space = 0

    def advance(self):
        if self.model.road_length <= self.pos[0] + self.model.space_between_cars + 1:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            self.available_space = self.get_available_space()
            self.model.grid.move_agent(self, (self.pos[0] + self.available_space, self.pos[1]))

    # def step(self):
    #     if self.pos[1] < self.model.lanes - 1 and self.no_space():
    #         self.switch_lane()
    #         if self.model.grid.is_cell_empty((self.pos[0], self.pos[1]+1)):
    #             pass
    #             #print("free lane above")
    #     #print(self.pos[0], self.pos[1])
    #         #print([list(x) for x in zip(*self.model.grid.grid)])
    #
    # def no_space(self):
    #     return True
    #
    # def switch_lane(self):
    #     return True

    def get_available_space(self):
        if self.first_run:
            return self.max_car_speed

        space = 0
        for i in range(1, self.model.road_length - self.pos[0]):
            if self.model.grid.is_cell_empty((self.pos[0] + i, self.pos[1])):
                space += 1
            else:
                break

        if space - self.model.space_between_cars > 0:
            space = space - self.model.space_between_cars
            if space > self.max_car_speed:
                space = self.max_car_speed
            return space
        return 0

class Obstacle(Agent):
    def __init__(self, unique_id, model, color):
        super(Obstacle, self).__init__(unique_id, model)
        self.color = color