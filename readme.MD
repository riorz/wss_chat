# Simple python websocket chat.
- require python3.7+
## Installation
```bash
python -m venv venv
pip install -e .
```
## Start a server
```bash
chatroom serve --bind-ip 0.0.0.0 --bind-port 8000 --ca-file certifications/cert_with_key.pem
```
## Start a client
```bash
chatroom connect --host localhost --bind-port 8000 --ca-file certifications/server.pem --handle your_name
```