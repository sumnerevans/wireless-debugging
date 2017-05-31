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
<<<<<<< HEAD
    hostname = from_config_yaml('hostname')
    port = from_config_yaml('port') or 80

=======
    hostname = from_config_yaml("hostname")
    port = from_config_yaml("port")
>>>>>>> WD-47, Added user managment interface classes, and a base class for having no authorization. Also modified controller to utilize functions in user management interface. Changed hostname and port to be defined in config.yaml, and obtained using from_config_yaml where it's called
    server = WSGIServer((hostname, port), bottle.default_app(),
                        handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
