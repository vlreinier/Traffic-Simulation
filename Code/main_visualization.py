from server import Server
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.datacollection import DataCollector
from model import Road
from agents import Vehicle, Obstacle
from random import choice


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Vehicle):
        portrayal["Color"] = "#e9ffe1"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["text"] = str(agent.unique_id) + agent.type
        portrayal["text_color"] = "black"
    if isinstance(agent, Obstacle):
        portrayal["Color"] = "grey"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal["text"] = agent.type
    return portrayal


grid = CanvasGrid(agent_portrayal, 100, 3, 1000, 300)
model_params = {
    "lanes": 3,
    "road_length": 100,
    "space_between_vehicles": 3,
    "obstacle_lane": UserSettableParameter(
        "choice", "obstacle baan", value=0, choices=[0, 1, 2], description=""
    ),
    "vehicle_frequency": UserSettableParameter(
        "choice", "Vehicle Frequency", value=0.05, choices=[0.05, 0.2, 0.5, 0.7], description=""
    ),
}
server = Server(Road, [grid], "Road Model", model_params)
server.launch(8521)
