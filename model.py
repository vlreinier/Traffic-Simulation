from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

import matplotlib.pyplot as plt
import numpy as np

class Road(Model):
    """A model with some number of agents."""
    def __init__(self, lanes, roadlength):
        self.grid = ContinuousSpace(x_max=roadlength, y_max=lanes, torus=False, x_min=0, y_min=0)
        import pdb; pdb.set_trace()
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.id = 0

        # # data collector
        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini},  # `compute_gini` defined above
        #     agent_reporters={"Wealth": "wealth"})


    def step(self):
        '''Advance the model by one step.'''
        # self.datacollector.collect(self)
        car = CarAgent(self.id, self)
        self.schedule.add(car)
        self.grid.place_agent(car, (1, 1))
        self.schedule.step()
        self.id += 1

class CarAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super(CarAgent, self).__init__(unique_id, model)
        self.wealth = 1

    def advance(self):
        self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))

    def move(self):
        self.advance()

    def step(self):
        self.move()


road = Road(1, 10)
for i in range(10):
    road.step()

# agent_counts = np.zeros((model.grid.width, model.grid.height))
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     agent_count = len(cell_content)
#     agent_counts[x][y] = agent_count
# plt.imshow(agent_counts, interpolation='nearest')
# plt.colorbar()
# plt.show()


# # Data collector
# gini = model.datacollector.get_model_vars_dataframe()
# plt.plot(gini)
# plt.show()

# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# print(agent_wealth)


# batch runner
# one_agent_wealth = agent_wealth.xs(14, level="AgentID")
# plt.plot(one_agent_wealth.Wealth)
# #plt.show()
#
#
# fixed_params = {
#     "width": 10,
#     "height": 10
# }
# variable_params = {"N": range(10, 500, 10)}
#
# # The variables parameters will be invoke along with the fixed parameters allowing for either or both to be honored.
# batch_run = BatchRunner(
#     MoneyModel,
#     variable_params,
#     fixed_params,
#     iterations=5,
#     max_steps=100,
#     model_reporters={"Gini": compute_gini}
# )
#
# batch_run.run_all()
#
# run_data = batch_run.get_model_vars_dataframe()
# plt.scatter(run_data.N, run_data.Gini)
# plt.show()