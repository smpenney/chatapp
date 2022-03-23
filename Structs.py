from enum import Enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json 

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
        if self.name == other.name:
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
