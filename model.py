from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid
from agents import CarAgent
from random import getrandbits

class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, road_length):
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.lanes = lanes
        self.road_length = road_length
        self.agent_id = 0
        self.grid = Grid(width=self.road_length, height=self.lanes, torus=False)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        for i in range(self.lanes):
            if getrandbits(1):
                car = CarAgent(self.agent_id, self)
                self.schedule.add(car)
                self.grid.place_agent(car, (0, i))
                self.id += 1


