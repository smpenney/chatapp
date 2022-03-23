import app
import socket
from threading import Thread

class Server():

    def __init__(self, port, logger):
        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = "127.0.0.1"
        self.port = port
        self.logger = logger
        
        self.me = app.Peer(name='SERVER', ip=self.ip, port=self.port, online=True)
        self.peers = [self.me]

        self.comms = app.Comms(self.me, self.me, logger)
        self.update_needed = False
