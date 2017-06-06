# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
WebSocket Controller
"""

import json
import time
import controller

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

    websocket_metadata = {}

    print('connection received')

    while not websocket.closed:
        try:
            message = websocket.receive()
            if message is None:
                continue

            decoded_message = json.loads(message)
            message_type = decoded_message['messageType']
            if message_type is None:
                # TODO: blow up
                pass

            new_metadata = _ws_routes[message_type](decoded_message, websocket,
                                                    websocket_metadata)

            if new_metadata is not None:
                websocket_metadata = {**websocket_metadata, **new_metadata}

        except WebSocketError:
            break

    if websocket in _web_interface_ws_connections:
        del _web_interface_ws_connections[websocket]


def ws_router(message_type):
    """ Provide a decorator for adding functions to the _ws_route dictionary """

    def decorator(function):
        _ws_routes[message_type] = function

    return decorator


@ws_router('startSession')
def start_session(message, websocket, metadata):
    """ Marks the start of a logging session,
        and attaches metadata to the websocket receiving the raw logs
    """

    metadata = {**metadata, **message}

    for key in ('apiKey', 'osType', 'deviceName', 'appName'):
        if key not in metadata:
            raise KeyError('startSession message requires %s parameter.' % key)

    return metadata


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

    api_key = metadata["apiKey"]

    # At first glance this looks like a copy,
    # but this is actually grabbing the keys from a dict
    web_ws_connections = [ws for ws in _web_interface_ws_connections]
    associated_websockets = (
        controller.user_management_interface.find_associated_websockets(
            api_key, web_ws_connections))

    for connection in associated_websockets:
        connection.send(util.serialize_json(parsed_logs))


@ws_router('endSession')
def end_session(message, websocket, metadata):
    print("currently defunct")


@ws_router('associateUser')
def associate_user(message, websocket, metadata):
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
