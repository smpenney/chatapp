import app
import socket
from threading import Thread

class Client():

    def __init__(self, name, client_port, server_ip, server_port, logger):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = client_port
        self.logger = logger
        
        self.me = app.Peer(
                            name=name, 
                            ip=self.ip,
                            port=self.port, 
                            online=False
                            )
        self.server = app.Peer(
                                name='SERVER', 
                                ip=server_ip, 
                                port=server_port, 
                                online=False
                                )
        self.peers = [self.me, self.server]

        self.comms = app.Comms(self.me, self.server, logger)

        self.shell()


    def shell(self):
        while True:
            message = {}
            data = input(">> ")

            if data.startswith("send_all "):
                parts = data.split()
                message = app.Message(
                    event_id=app.Events.BROADCAST,
                    sender=self.me,
                    recipient=self.server,
                    data=" ".join(parts[1:]),
                    ack=False,
                    timeout=0,
                    retries=0
                )
                self.comms.send(msg=message)

            # if data.startswith("send "):
            #     parts = data.split()
            #     message = Message(
            #         event_id=Events.DIRECT_MESSAGE,
            #         nickname=self.nickname,
            #         recipient=parts[1],
            #         data=" ".join(parts[2:]),
            #     )
            #     self.direct_message(message)
            #     continue

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
