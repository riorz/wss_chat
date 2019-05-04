import json
import asyncio
import websockets
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Server:
    USERS = dict() # Record all connected websockets.
    def __init__(self, host, port, ssl):
        self.host = host
        self.port = port
        self.ssl = ssl

    async def run(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                logger.info(f'receive message from websocket: {websocket}, broadcasting...')
                await self.broadcast(message, websocket, self.USERS[websocket])
        # XXX: add client close exception here. websockets.exceptions.ConnectionClosed
        finally:
            self.USERS.pop(websocket)

    async def register(self, websocket):
        """ Add connection to user list. """
        name = websocket.request_headers['handle']
        logger.info(f'Register user {name}: {websocket}')
        self.USERS[websocket] = name
        ok = json.dumps({'action': 'info', 'message': f'Hi, {name}'})
        await websocket.send(ok)

    async def broadcast(self, message, websocket, sender):
        """ Send message to all connected client. """
        if self.USERS:       # asyncio.wait doesn't accept an empty list
            for user in self.USERS.keys():
                msg = json.dumps({'action': 'broadcast', 'message': message, 'sender': sender})
                await user.send(msg)

    def start_server(self):
        logger.info('Starting server...')
        return websockets.serve(
            self.run, self.host, self.port, ssl=self.ssl
        )
