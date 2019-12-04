from server import Server
from mesa.visualization.modules import CanvasGrid
from model import Road


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal


max_car_length = 5
max_cars_per_lane = 30
space_between_cars = 5
grid_width = max_car_length * max_cars_per_lane
road_length = max_car_length * max_cars_per_lane * space_between_cars

grid = CanvasGrid(agent_portrayal, grid_width, grid_width, 700, 500)
server = Server(Road,
                [grid],
                "Road Model",
                {"lanes": 2, "road_length": road_length})
server.launch(8521)



