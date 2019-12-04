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


car_length = 5
road_length = 30
grid_width = car_length * road_length

grid = CanvasGrid(agent_portrayal, road_length, road_length / 2, 1000, 500)
server = Server(Road,
                [grid],
                "Road Model",
                {"lanes": 2, "roadlength": grid_width})
server.port = 8521
server.launch()



