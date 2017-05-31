#! /usr/bin/env python3

# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
WiDb Server Main Function
"""

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from helpers.util import from_config_yaml

import bottle

import controller
import parsing_lib

def main():
    hostname = from_config_yaml("hostname")
    port = from_config_yaml("port")
    server = WSGIServer((hostname, port), bottle.default_app(),
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
