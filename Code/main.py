from server import Server
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules.ChartVisualization import ChartModule
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


max_lanes = 6
road_length = 50
space_between_vehicles = 3
max_obstacles = 20
datacollector = DataCollector(
    model_reporters={
        "agent_count": lambda m: m.schedule.get_agent_count(),
        "speed": lambda m: m.get_avg_speed,
    }
)
grid = CanvasGrid(agent_portrayal, road_length, max_lanes, 1000, 300)
chart_agents = ChartModule(
    [{"Label": "agent_count", "Color": "red"}], data_collector_name="datacollector"
)
chart_speed = ChartModule(
    [{"Label": "speed", "Color": "black"}], data_collector_name="datacollector"
)
model_params = {
    "lanes": 3,
    "road_length": road_length,
    "space_between_vehicles": space_between_vehicles,
    "obstacles": UserSettableParameter(
        "choice", "obstacle baan", value=0, choices=[0, 1, 2], description=""
    ),
    "vehicle_frequency": UserSettableParameter(
        "choice", "Vehicle Frequency", value=0.05, choices=[0.05, 0.2, 0.5, 0.7], description=""
    ),
    "datacollector": datacollector,
}
server = Server(Road, [grid, chart_agents, chart_speed], "Road Model", model_params)
server.launch(8521)
