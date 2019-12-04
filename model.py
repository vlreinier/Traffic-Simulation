from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agents import CarAgent

class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, roadlength):
        self.grid = MultiGrid(width=roadlength, height=lanes, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.id = 0
        car = CarAgent(self.id, self)
        self.schedule.add(car)
        self.grid.place_agent(car, (0, 0))
        self.id += 1

    def step(self):
        '''Advance the model by one step.'''
        # self.datacollector.collect(self)
        self.schedule.step()
