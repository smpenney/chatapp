# Simple UDP Chat Client/Server

## Running

### Server

```python3 chat.py server -p {port number}```

### Client

```python3 chat.py client -n {name} -i {server IP} -p {server port} -c {client port}```

## Usage

### Commands:

reg {name} : Registers the current client with a new name
dereg {name} : De-registers the client with name {name}
send {client} {msg} : Sends a direct message {msg} to client {client}
send_all {msg} : Broadcasts {msg} to all clients
peers : Lists current chat peers


## Modifying

* Server will default to listening on 127.0.0.1 using the port given.  Update Server.py line 9 to set a new IP or allow for auto discovery of the IP.
* Logging mechanism is defined in chat.py.  It currently points to local files but could be modified to store in a local or remote database.
