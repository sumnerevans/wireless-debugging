#! /usr/bin/env python3
"""
WiDb Server Main Function
"""
import os
import argparse

import bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

import controller
from helpers.config_manager import ConfigManager
import parsing_lib


def main():
    os.chdir(os.path.dirname(__file__))
    hostname = ConfigManager.get('hostname')
    port = ConfigManager.get('port', 80)

    app = bottle.default_app()
    server = WSGIServer((hostname, port), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
