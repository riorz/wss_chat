#!/usr/bin/env python

import argparse
# from chatroom import server, client

parser = argparse.ArgumentParser(description='Start a server/client')

subparsers = parser.add_subparsers(dest='app', required=True)

client_parser = subparsers.add_parser('client')
client_parser.add_argument('--host', default='localhost', dest='host', type=str)
client_parser.add_argument('--bind-port', default='8000', dest='port', type=str)
client_parser.add_argument('--ca-file', dest='', help='path to certification file')
client_parser.add_argument('--handle', dest='handle', type=str)

server_parser = subparsers.add_parser('server')
server_parser.add_argument('--bind-ip', default='0.0.0.0', dest='ip', type=str)
server_parser.add_argument('--bind-port', default='8000', dest='port', type=str)
server_parser.add_argument('--ca-file', dest='', help='path to certification file')

args = parser.parse_args()