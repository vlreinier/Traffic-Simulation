from server import Server
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from model import Road
from agents import Car, Obstacle


def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Car):
        portrayal["Color"] = agent.color
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.1
    if isinstance(agent, Obstacle):
        portrayal["Color"] = 'red'
        portrayal["Shape"] = 'circle'
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.9
    return portrayal


lanes = 10
road_length = 100
space_between_cars = 3
grid = CanvasGrid(agent_portrayal, road_length, lanes, 900, 300)

model_params = {"lanes": UserSettableParameter("slider", "Lanes", 3, 1, lanes,
                                                    description=""),
                "road_length": road_length,
                "space_between_cars": space_between_cars,
                "obstacles": UserSettableParameter("slider", "Random Obstacles", 1, 0, 10, 1,
                                                    description=""),
                "car_frequency": UserSettableParameter("slider", "Car Increase Frequency", 0.3, 0.05, 0.95, 0.05,
                                                    description="")
                }

server = Server(Road,
                [grid],
                "Road Model",
                model_params)
server.launch(8521)



