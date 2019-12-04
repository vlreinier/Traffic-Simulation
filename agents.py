from mesa import Agent


class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super(CarAgent, self).__init__(unique_id, model)

    def advance(self):
        if self.pos[0] + 2 < self.model.grid.width:
            self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))



