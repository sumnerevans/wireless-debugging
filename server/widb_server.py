#! /usr/bin/env python3

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
from datastore_interfaces import *

#global variable
datastore_interface = mongo_datastore_interface.MongoDatastoreInterface()

def main():
    hostname = from_config_yaml("hostname")
    port = from_config_yaml("port")
    server = WSGIServer((hostname, port), bottle.default_app(),
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
