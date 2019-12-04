from server import Server
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import Road
from agents import CarAgent


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, CarAgent):
        portrayal["Color"] = agent.color
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.1
    return portrayal


lanes = 5
road_length = 100
grid = CanvasGrid(agent_portrayal, road_length, lanes, 1000, 300)


model_params = {"lanes": UserSettableParameter("slider", "Lanes", 2, 1, 5,
                                                    description=""),
                "road_length": road_length,
                "car_frequency": UserSettableParameter("slider", "Car Frequency", 50, 10, 90, 10,
                                                    description="")
                }

server = Server(Road,
                [grid],
                "Road Model",
                model_params)
server.launch(8521)



