from mesa import Agent


class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, max_car_speed, color, first_run):
        super(CarAgent, self).__init__(unique_id, model)
        self.max_car_speed = max_car_speed
        self.color = color
        self.first_run = first_run

    def advance(self):
        available_space = self.get_available_space()
        if self.pos[0] + available_space < self.model.grid.width:
            self.model.grid.move_agent(self, (self.pos[0] + available_space, self.pos[1]))
        else:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

    def get_available_space(self):
        # if first run always replace with max speed
        if self.first_run:
            return self.max_car_speed

        # else calculate available space
        space = 0
        for i in range(1, 10):
            if self.model.grid.is_cell_empty((self.pos[0] + i, self.pos[1])): space += 1
            else: break
        if space - self.model.space_between_cars > 0:
            space = space - self.model.space_between_cars
            if space > self.max_car_speed:
                space = self.max_car_speed
            return space
        else:
            return 0
