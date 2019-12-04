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


grid = CanvasGrid(agent_portrayal, 50, 50, 1000, 500)
server = Server(Road,
                [grid],
                "Road Model",
                {"lanes":2, "roadlength": 1000}
            )
server.port = 8521 # The default
server.launch()



