from queue import Queue
import socket
from threading import Thread
from Structs import Events, Message, Peer
from Global import *

class Comms:
    def __init__(self, me, server, logger) -> None:
        self.update_needed = False
        self.acks = {}
        self.input_queue = Queue()
        self.me = me
        self.server = server
        self.peers = [me, server]
        self.logger = logger

        self.start()

    def start(self):
        self.comm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.comm.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.comm.bind((self.me.ip, self.me.port))
        self.logger.info(f"{self.me.name}: {self.me.ip}:{self.me.port}")

        Thread(target=self.receiver_thread).start()

    def stop(self):
        self.comm.close()

    def receiver_thread(self):
        self.logger.info(
            f"RECEIVER_THREAD: {self.me.name} -> {self.me.ip}:{self.me.port}")
        while True:
            data, addr = self.comm.recvfrom(MSG_SIZE)
            self.input_queue.put((data, addr))

    def get_peer(self, name):
        for p in self.peers:
            if p.name == name:
                return p
        return None

    def send(self, msg):
        # if ack:
        #     self.track_ack(msg)
        print(msg)
        self.comm.sendto(msg.to_json().encode('utf-8'),
                         (msg.recipient.ip, msg.recipient.port))
        # if ack and verify:
        #     return self.check_ack_timeout(msg, timeout, retries)
        # if verify and not ack:
        #     self.logger.debug(f"IGNORE:  Verify w/o Track for {msg}")
        # return True
