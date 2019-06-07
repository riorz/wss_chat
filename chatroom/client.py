import asyncio
import websockets
import logging
import functools
from contextlib import suppress
from .display import Display, AsyncPrompt
import json

logger = logging.getLogger(f'{__name__}.client')


class Client:
    def __init__(self, path: str, port: int, ssl, handle: str, loop):
        self.url = f'wss://{path}:{port}'
        self.ssl = ssl
        self.loop = loop
        self.handle = handle
        self.display = Display()
        self.closed = False
        self.raw_input = functools.partial(AsyncPrompt(), end='', flush=True)

    async def connect(self):
        logger.info(f'Connecting to {self.url}...')
        self.websocket = await websockets.connect(self.url, ssl=self.ssl,
                                                  extra_headers={'handle': self.handle})

    async def input_message(self):
        self.display.wait_input()
        input = await self.raw_input(f'{self.handle}: ')
        if input == '!quit':
            await self.websocket.close(reason='bye')
            self.closed = True
            logger.info('User quit.')
            return
        await self.websocket.send(input)

    async def receive_message(self):
        try:
            msg = await self.websocket.recv()
            logger.info(f'receive message: {msg}')
            msg = json.loads(msg)
            if msg['action'] == 'info':
                self.display.print(f'server: {msg["message"]}')
            elif msg['action'] == 'broadcast':
                self.display.print(f'{msg["sender"]}: {msg["message"]}')
        except websockets.exceptions.ConnectionClosed as e:
            logger.info(f'Connection closed: <{e.code}>: {e.reason}')
            self.closed = True

    async def run(self):
        await self.connect()
        self.display.clear()
        while not self.closed:
            on_input = asyncio.create_task(self.input_message())
            on_receive = asyncio.create_task(self.receive_message())
            _, pending = await asyncio.wait(
                {on_input, on_receive},
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()

    async def close(self):
        """ clean up tasks """
        pending = asyncio.Task.all_tasks()
        for task in pending:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        self.loop.stop()
