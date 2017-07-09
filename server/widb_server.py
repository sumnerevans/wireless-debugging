#! /usr/bin/env python3
"""
WiDb Server Main Function
"""
import os

import bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

# Import the application.
import controller
from helpers.config_manager import ConfigManager


def main():
    # Change the working directory to where this file is (in this case, the
    # /server folder.) This allows all of the relative paths to work throughout
    # the application.
    os.chdir(os.path.dirname(__file__))

    # Retrieve the configuration from the ConfigManager.
    hostname = ConfigManager.get('hostname')
    port = ConfigManager.get('port', 80)

    app = bottle.default_app()
    server = WSGIServer((hostname, port), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
