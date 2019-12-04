from mesa import Agent


class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, max_car_speed, color):
        super(CarAgent, self).__init__(unique_id, model)
        self.max_car_speed = max_car_speed
        self.color = color

    def advance(self):
        if self.pos[0] + self.max_car_speed < self.model.grid.width:
            space_available = 0
            for i in range(self.max_car_speed):
                if self.model.grid.is_cell_empty((self.pos[0] + 1, self.pos[1])):
                    space_available += 1
            self.model.grid.move_agent(self, (self.pos[0] + space_available, self.pos[1]))
        else:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
