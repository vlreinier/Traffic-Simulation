from server import Server
from mesa.visualization.modules import CanvasGrid
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


max_car_length = 3
max_cars_per_lane = 20
space_between_cars = 2
lanes = 4

road_length = max_cars_per_lane * (max_car_length + space_between_cars)
grid = CanvasGrid(agent_portrayal, road_length, lanes, 1000, 500)
server = Server(Road,
                [grid],
                "Road Model",
                {"lanes": lanes, "road_length": road_length})
server.launch(8521)



