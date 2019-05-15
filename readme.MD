# Simple python websocket chat.
- require python3.7+
## Installation
```bash
python -m venv venv
. venv/bin/activate
pip install .
```
## Start a server
```bash
chatroom serve --bind-ip 0.0.0.0 --bind-port 8000 --ca-file certifications/cert_with_key.pem [--allowed-clients folder_contains_client_cert]
```
## Start a client
```bash
chatroom connect --host localhost --bind-port 8000 --ca-file certifications/server.pem --handle your_name [--client-cert client_cert/client.pem]
```