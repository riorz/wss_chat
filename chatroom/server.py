#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# XXX: Refactor to server class?

User = namedtuple('User', ['name','websocket'])
USERS = set() # Record all connected websockets.

async def echo(websocket, path):
    user = await register(websocket)
    try:
        async for message in websocket:
            logger.info(f'receive message from websocket: {websocket}, broadcasting...')
            await broadcast(message, websocket)
    # XXX: add client close exception here. websockets.exceptions.ConnectionClosed
    finally:
        USERS.remove(user)


async def register(websocket):
    """ Add connection to user list. """
    await websocket.send('Please enter your name')
    name = await websocket.recv()
    user = User(name, websocket)
    logger.info(f'Register user {name}: {websocket}')
    USERS.add(user)
    await websocket.send(f'Hi, {name}')
    return user


async def broadcast(message, websocket):
    """ Send message to all connected client. """
    if USERS:       # asyncio.wait doesn't accept an empty list
        for user in USERS:
            # XXX: maybe send messages in JSON?
            # like {action: "broadcast", message: "message", sender: "user_name"}
            await user.websocket.send(message)


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name('server.pem'),
    pathlib.Path(__file__).with_name('server.key'))

start_server = websockets.serve(
    echo, '127.0.0.1', 8765, ssl=ssl_context)

logger.info('start server...')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()