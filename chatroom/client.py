#!/usr/bin/env python

import asyncio
import pathlib
import ssl
import websockets
import logging
import functools
from prompt import AsyncPrompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('server.pem'))

prompt = AsyncPrompt()
raw_input = functools.partial(prompt, end='', flush=True)


class Client:
    def __init__(self, path, port, ssl, loop):
        self.url = f'wss://{path}:{port}'
        self.ssl = ssl
        self.loop = loop

    async def connect(self):
        logger.info(f'Connecting to {self.url}...')
        self.websocket = await websockets.connect(self.url, ssl=self.ssl)

    async def input_message(self):
        input = await raw_input('> ')
        await self.websocket.send(input)

    async def print_message(self):
        msg = await self.websocket.recv()
        print(f'\n< {msg}')

    async def run(self):
        stop = False
        await self.connect()
        while not stop:
            try:
                on_input = asyncio.create_task(self.input_message())
                on_receive = asyncio.create_task(self.print_message())
                _, pending = await asyncio.wait(
                    {on_input, on_receive},
                    return_when=asyncio.FIRST_COMPLETED
                )
                for task in pending:
                    task.cancel()
            except KeyboardInterrupt:
                logger.info('user shut down')
                stop = True
                break


loop = asyncio.get_event_loop()
client = Client('localhost', '8765', ssl_context, loop)
loop.run_until_complete(client.run())
