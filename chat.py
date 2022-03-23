from ipaddress import ip_address
from sys import int_info

import argparse
import logging
from Server import Server
from Client import Client
from Global import *
from Structs import Peer, Message, Events


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
            Server(args.port, logger)
        else:
            print("-p/--port is required for server startup")
    elif args.mode == "client":
        if (
            args.name is not None
            and args.client_port is not None
            and args.ip is not None
        ):
            Client(args.name, args.client_port,
                          args.ip, args.port, logger)
        else:
            print("-p/port, -i/ip, and -n/name are all required for client startup")


if __name__ == "__main__":
    main()
