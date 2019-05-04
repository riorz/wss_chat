# Simple python websocket chat.
- require python3.7+
## Installation
```bash
python -m venv venv
pip install -r requirements.txt
```
## Start a server
```bash
python app.py server --bind-ip 0.0.0.0 --bind-port 8000 --ca-file certifications/cert_with_key.pem
```
## Start a client
```bash
python app.py client --host localhost --bind-port 8000 --ca-file certifications/server.pem --handle your_name
```