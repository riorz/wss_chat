#!/usr/bin/env python

import argparse
import pathlib
import ssl
import asyncio
from chatroom import server, client

parser = argparse.ArgumentParser(description='Start a server/client')

subparsers = parser.add_subparsers(dest='app', required=True)

client_parser = subparsers.add_parser('client')
client_parser.add_argument('--host', dest='host', type=str, default='localhost')
client_parser.add_argument('--bind-port', dest='port', type=int, default=8000)
client_parser.add_argument('--ca-file', type=pathlib.Path, required=True)
client_parser.add_argument('--handle', dest='handle', type=str, required=True)

server_parser = subparsers.add_parser('server')
server_parser.add_argument('--bind-ip', dest='ip', type=str, default='0.0.0.0')
server_parser.add_argument('--bind-port', dest='port', type=int, default=8000)
server_parser.add_argument('--ca-file', type=pathlib.Path, required=True)


def get_ssl_context(app_type, path):
    """ Return ssl_context by type """
    protocol = {
        'client': ssl.PROTOCOL_TLS_CLIENT,
        'server': ssl.PROTOCOL_TLS_SERVER,
    }[app_type]
    ssl_context = ssl.SSLContext(protocol)

    if app_type == 'server':
        ssl_context.load_cert_chain(path)
    elif app_type == 'client':
        ssl_context.load_verify_locations(path)

    return ssl_context


args = parser.parse_args()
ssl_context = get_ssl_context(args.app, args.ca_file)
loop = asyncio.get_event_loop()

if args.app == 'server':
    app = server.Server(args.ip, args.port, ssl=ssl_context)
    loop.run_until_complete(app.start_server())
    loop.run_forever()
elif args.app == 'client':
    app = client.Client(args.host, args.port, ssl_context, args.handle, loop)
    loop.run_until_complete(app.run())
