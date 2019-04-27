#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

USERS = set()

async def echo(websocket, path):
    # Register.
    USERS.add(websocket)
    try:
        async for message in websocket:
            print('receive:', message)
            logger.info(f'receive message from websocket: {websocket}, broadcasting...')
            await broadcast(message, websocket)
    finally:
        USERS.remove(websocket)


async def broadcast(message, websocket):
    if USERS:       # asyncio.wait doesn't accept an empty list
        for user in USERS:
            await user.send(message)
        #await asyncio.wait([user.send(message) for user in USERS])


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name('server.pem'),
    pathlib.Path(__file__).with_name('server.key'))

start_server = websockets.serve(
    echo, 'localhost', 8765, ssl=ssl_context)

logger.info('start server...')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()