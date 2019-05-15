#!/usr/bin/env python

import argparse
import pathlib
import ssl
import asyncio
import logging
from chatroom import server, client

logging.basicConfig(
    filename='chatroom.log',
    level=logging.INFO,
    format='%(asctime)s %(name)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S'
)
logger = logging.getLogger(__name__)


def get_ssl_context(app_type, path, **kwargs):
    """ Return ssl_context by type """
    protocol = {
        'client': ssl.PROTOCOL_TLS_CLIENT,
        'server': ssl.PROTOCOL_TLS_SERVER,
    }[app_type]
    ssl_context = ssl.SSLContext(protocol)

    if app_type == 'server':
        ssl_context.load_cert_chain(path)
        if 'client_cert' in kwargs.keys():
            logger.info('client authentication needed.')
            ssl_context.load_verify_locations(capath=kwargs['client_cert'])
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            logger.info(ssl_context.verify_mode)

    elif app_type == 'client':
        ssl_context.load_verify_locations(path)
        if 'client_cert' in kwargs.keys():
            ssl._create_default_https_context = ssl._create_unverified_context
            ssl_context.load_cert_chain(kwargs['client_cert'])

    return ssl_context


def main():
    parser = argparse.ArgumentParser(description='Start a server/client')
    subparsers = parser.add_subparsers(dest='action', required=True)

    # client commands
    client_parser = subparsers.add_parser('connect')
    client_parser.add_argument(
        '--host', dest='host', type=str, default='localhost')
    client_parser.add_argument(
        '--bind-port', dest='port', type=int, default=8000)
    client_parser.add_argument('--ca-file', type=pathlib.Path, required=True)
    client_parser.add_argument(
        '--handle', dest='handle', type=str, required=True)
    client_parser.add_argument(
        '--client-cert', type=pathlib.Path, required=False)

    # server commands
    server_parser = subparsers.add_parser('serve')
    server_parser.add_argument(
        '--bind-ip', dest='ip', type=str, default='0.0.0.0')
    server_parser.add_argument(
        '--bind-port', dest='port', type=int, default=8000)
    server_parser.add_argument('--ca-file', type=pathlib.Path, required=True)
    server_parser.add_argument('--allowed-clients', type=pathlib.Path,
                               dest='client_cert', required=False)

    args = parser.parse_args()
    app_type = {
        'serve': 'server',
        'connect': 'client',
    }[args.action]
    ssl_context = get_ssl_context(app_type, args.ca_file,
                                  client_cert=args.client_cert)
    loop = asyncio.get_event_loop()

    if app_type == 'server':
        logger.info('Start a server...')
        app = server.Server(args.ip, args.port, ssl=ssl_context)
        loop.run_until_complete(app.start_server())
        loop.run_forever()
    elif app_type == 'client':
        logger.info('Start a client...')
        app = client.Client(args.host, args.port,
                            ssl_context, args.handle, loop)
        try:
            loop.run_until_complete(app.run())
        except KeyboardInterrupt:
            logger.info('Keyboard Interrupted.')
        finally:
            logger.info('Closing client')
            loop.run_until_complete(app.close())
            loop.close()
