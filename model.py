from mesa import Agent, Model
from server import Server
from mesa.visualization.modules import CanvasGrid

from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

import matplotlib.pyplot as plt
import numpy as np

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

        print("test")

class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super(CarAgent, self).__init__(unique_id, model)

    def advance(self):
        if self.pos[0] + 2 < self.model.grid.width:
            self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))



def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 300, 300)
server = Server(Road,
                [grid],
                "Money Model",
                {"lanes":1, "roadlength": 1000}
            )
server.port = 8521 # The default
server.launch()



