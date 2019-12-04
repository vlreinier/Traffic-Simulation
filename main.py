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
max_cars = 30
space_between_cars = 5
grid_width = car_length * road_length * space_between_cars

grid = CanvasGrid(agent_portrayal, max_car_length*max_cars, max_car_length*max_cars, 700, 500)
server = Server(Road,
                [grid],
                "Road Model",
                {"lanes": 2, "road_length": grid_width})
server.launch(8521)



