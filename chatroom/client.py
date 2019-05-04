import asyncio
import websockets
import logging
import functools
from .prompt import AsyncPrompt
from .display import Display
import json
import time

logging.basicConfig(
    filename='client.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('client')

prompt = AsyncPrompt()
raw_input = functools.partial(prompt, end='', flush=True)

class Client:
    def __init__(self, path, port, ssl, handle, loop):
        self.url = f'wss://{path}:{port}'
        self.ssl = ssl
        self.loop = loop
        self.handle = handle
        self.display = Display()

    async def connect(self):
        logger.info(f'Connecting to {self.url}...')
        self.websocket = await websockets.connect(self.url, ssl=self.ssl,
                                                  extra_headers={'handle': self.handle})

    async def input_message(self):
        self.display.wait_input()
        input = await raw_input('you: ')
        await self.websocket.send(input)

    async def receive_message(self):
        msg = await self.websocket.recv()
        logger.info(f'receive message: {msg}')
        msg = json.loads(msg)
        if msg['action'] == 'info':
            self.display.print(f'server: {msg["message"]}')
        elif msg['action'] == 'broadcast':
            self.display.print(f'{msg["sender"]}: {msg["message"]}')

    async def run(self):
        stop = False
        await self.connect()
        self.display.clear()
        while not stop:
            try:
                on_input = asyncio.create_task(self.input_message())
                on_receive = asyncio.create_task(self.receive_message())
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
