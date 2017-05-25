#! /usr/bin/env python3

"""
WiDb Server Main Function
"""

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

import bottle

import controller
import parsing_lib

def main():
    server = WSGIServer(("0.0.0.0", 80), bottle.default_app(),
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
