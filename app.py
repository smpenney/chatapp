from ipaddress import ip_address
import socket
import os
from sys import int_info
import time
import datetime
from enum import Enum
from dataclasses import dataclass, InitVar
from dataclasses_json import dataclass_json
import argparse
from threading import Thread
from queue import Queue
import json
import logging
import Server
import Client

MSG_SIZE = 4096
TIMEOUT_DEREG = 500
RETRY_DEREG = 5
TIMEOUT_MESSAGE = 500
RETRY_MESSAGE = 2


class Events(Enum):
    REGISTER = 1
    DEREGISTER = 2
    REGISTER_CONFIRM = 3
    DEREGISTER_CONFIRM = 4
    CLIENT_UPDATE = 5

    BROADCAST = 10
    DIRECT_MESSAGE = 11
    OFFLINE_MESSAGE = 12

    PING = 97
    ERROR = 98
    ACK = 99


@dataclass_json
@dataclass
class Peer:
    name: str
    ip: str
    port: int
    online: bool
    offline_messages = []

    def __str__(self):
        status = "ONLINE" if self.online else "OFFLINE"
        return f"{self.name} @ {self.ip}:{self.port} is {status}"

    def __eq__(self, other) -> bool:
        if self.sender == other.sender:
            return True
        return False

    def __hash__(self):
        return hash((self.name, self.ip, self.port))


@dataclass_json
@dataclass
class Message:
    event_id: Events
    sender: Peer
    recipient: Peer = None
    data: str = None
    hash: int = None
    ack: bool = False
    timeout: int = None
    retries: int = None

    def __post_init__(self):
        if self.hash == None:
            self.hash = hash(
                (self.event_id, self.sender, self.data, self.recipient))

    def __str__(self):
        return f"{self.event_id}|{self.sender}|{self.recipient}|{self.data}|{self.hash}"


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


def get_args():
    parser = argparse.ArgumentParser("Chat Application")
    parser.add_argument(
        "mode",
        choices=["client", "server"],
        help="assign role - client or server",
    )
    parser.add_argument("-n", "--name", help="name of the client", type=str)
    parser.add_argument(
        "-i",
        "--ip",
        help="specify ip for the server",
        type=str)
    parser.add_argument(
        "-p",
        "--port",
        help="specify port of the server",
        type=int)
    parser.add_argument(
        "-c",
        "--client_port",
        help="client port to bind to",
        type=int)
    return parser.parse_args()


def setup_logger():
    logger = logging.getLogger("ChatApp")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s|%(name)s|%(levelname)s|%(message)s")

    info_handler = logging.StreamHandler()
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    debug_handler = logging.FileHandler(filename="ChatApp.log", mode="a")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)

    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)

    return logger


def main():
    logger = setup_logger()
    args = get_args()
    if args.mode == "server":
        if args.port is not None:
            Server.Server(args.port, logger)
        else:
            print("-p/--port is required for server startup")
    elif args.mode == "client":
        if (
            args.name is not None
            and args.client_port is not None
            and args.ip is not None
        ):
            Client.Client(args.name, args.client_port,
                          args.ip, args.port, logger)
        else:
            print("-p/port, -i/ip, and -n/name are all required for client startup")


if __name__ == "__main__":
    main()
