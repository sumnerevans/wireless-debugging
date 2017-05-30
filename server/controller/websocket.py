# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
WebSocket Controller
"""

import json
import time

from bottle import route, request, abort
from geventwebsocket import WebSocketError

from parsing_lib import LogParser
from helpers import util

# Store a dictionary of string -> function
_ws_routes = {}
_web_interface_ws_connections = []


@route('/ws')
def handle_websocket():
    """ Handle an incomming WebSocket connection.

    This function handles incomming WebSocket connections and waits for
    incomming messages from the connection. When a message is recieved, it
    calls the appropriate function.
    """

    websocket = request.environ.get('wsgi.websocket')
    if not websocket:
        abort(400, 'Expected WebSocket request.')

    print('connection received')

    while not websocket.closed:
        try:
            message = websocket.receive()
            if message is None:
                continue

            decoded_message = json.loads(message)
            messageType = decoded_message['messageType']
            if messageType is None:
                # TODO: blow up
                pass

            _ws_routes[messageType](decoded_message, websocket)
        except WebSocketError:
            break

    # Remove the WebSocket connection from the list once it is closed
    _web_interface_ws_connections.remove(websocket)


def ws_router(messageType):
    """ Provide a decorator for adding functions to the _ws_route dictionary """

    def decorator(function):
        _ws_routes[messageType] = function

    return decorator


@ws_router('logDump')
def log_dump(message, websocket):
    """ Handles Log Dumps from the Mobile API

    When a log dump comes in from the Mobile API, this function takes the raw
    log data, parses it and sends the parsed data to all connected web clients.

    Args:
        message: the decoded JSON message from the Mobile API
        websocket: the full websocket connection
    """
    parsed_logs = LogParser.parse(message)

    for connection in _web_interface_ws_connections:
        connection.send(util.serialize_to_json(parsed_logs))


@ws_router('associateSession')
def associate_session(message, websocket):
    """ Associates a WebSocket connection with a session

    When a browser requests to be associated with a session, add the associated
    WebSocket connection to the list connections for that session.

    Args:
        message: the decoded JSON message from the Mobile API
        websocket: the full websocket connection
    """

    # TODO: Currently we only have one session, when we implement multiple
    #       connections, modify this to handle it
    _web_interface_ws_connections.append(websocket)
