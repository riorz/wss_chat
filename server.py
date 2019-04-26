#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        print(message)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    pathlib.Path(__file__).with_name('server.pem'),
    pathlib.Path(__file__).with_name('server.key'))

start_server = websockets.serve(
    echo, 'localhost', 8765, ssl=ssl_context)

logger.info('start server...')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()