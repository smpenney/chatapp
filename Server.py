import Comms
from Global import *
from Structs import Peer, Message, Events


class Server():

    def __init__(self, port, logger):
        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = "127.0.0.1"
        self.port = port
        self.logger = logger

        self.me = Peer(name='SERVER', ip=self.ip,
                           port=self.port, online=True)
        self.peers = [self.me]

        self.comms = Comms.Comms(self.me, self.me, logger)
        self.update_needed = False

        self.watch_queue()

    def watch_queue(self):
        while True:
            # if self.update_needed or self.comms.update_needed:
            #     self.update_clients()
            while not self.comms.input_queue.empty():
                data, addr = self.comms.input_queue.get()
                self.logger.debug(f"RECEIVED: {addr}: {data.decode()}")
                msg = Message.from_json(data.decode('utf-8'))
                self.handle_message(msg)

    def handle_message(self, msg):
        self.logger.debug(f'{self.me.name}: {msg}')
        if msg.event_id in [Events.BROADCAST]:
            self.comms.broadcast(msg)

        if msg.event_id in [Events.DIRECT_MESSAGE]:
            pass
