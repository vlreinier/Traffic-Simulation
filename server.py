import os
import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import tornado.gen
import webbrowser
from mesa.visualization.ModularVisualization import ModularServer


class Server(ModularServer):
    def launch(self, port=None):
        """ Run the app. """
        if port is not None:
            self.port = port
        url = 'http://127.0.0.1:{PORT}'.format(PORT=self.port)
        print('Interface starting at {url}'.format(url=url))
        self.listen(self.port)
        tornado.autoreload.start()
        tornado.ioloop.IOLoop.current().start()