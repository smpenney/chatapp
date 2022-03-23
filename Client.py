import Comms
import socket
from threading import Thread
from Global import *
from Structs import Peer, Message, Events


class Client():

    def __init__(self, name, client_port, server_ip, server_port, logger):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = client_port
        self.logger = logger

        self.me = Peer(
            name=name,
            ip=self.ip,
            port=self.port,
            online=False
        )

        self.server = Peer(
            name='SERVER',
            ip=server_ip,
            port=server_port,
            online=False
        )

        self.comms = Comms.Comms(self.me, self.server, logger)

        Thread(target=self.watch_queue).start()
        self.shell()

    def watch_queue(self):
        while True:
            while not self.comms.input_queue.empty():
                data, addr = self.comms.input_queue.get()
                self.logger.debug(f"RECEIVED: {addr}: {data.decode()}")
                msg = Message.from_json(data.decode('utf-8'))
                self.handle_message(msg)

    def handle_message(self, msg):
        self.logger.debug(f'{self.me.name}: {msg}')
        print(msg)

    def shell(self):
        while True:
            message = {}
            data = input(">> ")

            if data.startswith("send_all "):
                parts = data.split()
                message = Message(
                    event_id=Events.BROADCAST,
                    sender=self.me,
                    recipient=self.server,
                    data=" ".join(parts[1:]),
                    ack=False,
                    timeout=0,
                    retries=0
                )
                self.comms.send(msg=message)

            if data.startswith("send "):
                parts = data.split()
                peer = self.comms.get_peer(parts[1])
                if peer is not None:
                    message = Message(
                        event_id=Events.DIRECT_MESSAGE,
                        sender=self.me,
                        recipient=peer,
                        data=" ".join(parts[2:]),
                        ack = False,
                        timeout = 0,
                        retries = 0
                    )
                    self.comms.send(msg=message)
                else:
                    print(f"Unknown peer: {parts[1]}")
                continue

            elif data == "":
                continue

            # elif data == "peers":
            #     self.show_peers()
            #     continue

            # elif data.startswith("dereg"):
            #     parts = data.split()
            #     if len(parts) != 1:
            #         self.deregister(parts[1])
            #     else:
            #         print("USAGE: dereg {nickname}")

            # elif data.startswith("reg"):
            #     parts = data.split()
            #     if len(parts) != 1:
            #         self.register(parts[1])
            #     else:
            #         print("USAGE: reg {nickname}")

            # elif data == "quit":
            #     self.deregister(self.nickname)
            #     break

        # self.client.close()
        # os._exit(1)
