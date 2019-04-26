import asyncio
import websockets
import pathlib
import ssl
import logging

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_verify_locations(
    pathlib.Path(__file__).with_name('server.pem'))

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

async def start_server(path, port, ssl_context):
    logger.info('Start server...')
    conn = await websockets.serve(hello, path, port, ssl=ssl_context)
    return conn

async def hello(websocket):
    name = await websocket.recv()
    print(f'< {name}')

    await websocket.send(name)
    print(f'> {name}')

    greeting = await websocket.recv()
    print(f'< {greeting}')

# start_server = websockets.serve(hello, 'localhost', 1234, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server('localhost', '1234', ssl_context))
asyncio.get_event_loop().run_forever()