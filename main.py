from server import Server
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import Road
from agents import Vehicle, Obstacle
from random import choice


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Vehicle):
        portrayal["Color"] = '#e9ffe1'
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal['text'] = str(agent.unique_id)+ agent.type
        portrayal['text_color'] = 'black'
    if isinstance(agent, Obstacle):
        portrayal["Color"] = 'grey'
        portrayal["Shape"] = 'rect'
        portrayal["Filled"] = "false"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        portrayal['text'] = agent.type
    return portrayal


max_lanes = 6
road_length = 50
space_between_vehicles = 4
max_obstacles = 20
grid = CanvasGrid(agent_portrayal, road_length, max_lanes, 1000, 300)

model_params = {"lanes": UserSettableParameter("slider", "Lanes", 3, 1, max_lanes,
                                                    description=""),
                "road_length": road_length,
                "space_between_vehicles": space_between_vehicles,
                "obstacles": UserSettableParameter("slider", "Random Obstacles", 2, 0, max_obstacles, 1,
                                                    description=""),
                "vehicle_frequency": UserSettableParameter("slider", "Vehicle Frequency", 0.2, 0.05, 1, 0.05,
                                                    description="")
                }

server = Server(Road,
                [grid],
                "Road Model",
                model_params)
server.launch(8521)



