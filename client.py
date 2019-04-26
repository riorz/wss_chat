#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets
import logging

logging.basicConfig()
logger = logging.getLogger('client')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('server.pem'))


async def start_server(path, port, ssl):
    url = f'wss://{path}:{port}'
    websocket = await websockets.connect(url, ssl=ssl)
    return websocket

async def greet(websocket):
    name = input("What's your name? ")

    await websocket.send(name)
    print(f"> {name}")

    greeting = await websocket.recv()
    print(f"< {greeting}")

async def run(websocket):
    while True:
        try:
            msg = input("you:")
            await websocket.send(msg)
            message = await websocket.recv()
            print(message)
        except KeyboardInterrupt:
            websocket.close()
            logger.info('bye')
            break


loop = asyncio.get_event_loop()
tasks = start_server('localhost', '8765', ssl_context)
conn = loop.run_until_complete(tasks)
loop.run_until_complete(greet(conn))
loop.run_until_complete(run(conn))
loop.run_forever()