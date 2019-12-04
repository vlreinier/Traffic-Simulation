from server import Server
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import Road
from agents import CarAgent


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, CarAgent):
        portrayal["Color"] = agent.color
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.9
    return portrayal


max_cars_per_lane = 20
space_between_cars = 3
lanes = 5
road_length = max_cars_per_lane * space_between_cars
grid = CanvasGrid(agent_portrayal, road_length, lanes, 1000, 500)


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



