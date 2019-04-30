#!/usr/bin/env python

import json
import asyncio
import pathlib
import ssl
import websockets
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

USERS = dict() # Record all connected websockets.

async def echo(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            logger.info(f'receive message from websocket: {websocket}, broadcasting...')
            await broadcast(message, websocket, USERS[websocket])
    # XXX: add client close exception here. websockets.exceptions.ConnectionClosed
    finally:
        USERS.pop(websocket)


async def register(websocket):
    """ Add connection to user list. """
    msg = json.dumps({'action': 'info', 'message': 'Please enter your name'})
    await websocket.send(msg)
    name = await websocket.recv()
    logger.info(f'Register user {name}: {websocket}')
    USERS[websocket] = name
    ok = json.dumps({'action': 'info', 'message': f'Hi, {name}'})
    await websocket.send(ok)


async def broadcast(message, websocket, sender):
    """ Send message to all connected client. """
    if USERS:       # asyncio.wait doesn't accept an empty list
        for user in USERS.keys():
            msg = json.dumps({'action': 'broadcast', 'message': message, 'sender': sender})
            await user.send(msg)


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name('server.pem'),
    pathlib.Path(__file__).with_name('server.key'))

start_server = websockets.serve(
    echo, '127.0.0.1', 8765, ssl=ssl_context)

logger.info('start server...')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()