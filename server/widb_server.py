#! /usr/bin/env python3
"""
WiDb Server Main Function
"""
import os

import bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

import controller
from helpers.util import from_config_yaml
import parsing_lib


def main():
    os.chdir(os.path.dirname(__file__))
    hostname = from_config_yaml('hostname')
    port = from_config_yaml('port') or 80

    server = WSGIServer((hostname, port), bottle.default_app(),
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
