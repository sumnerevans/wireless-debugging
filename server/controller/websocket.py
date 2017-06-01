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
_ws_routes = {} # pylint: disable=invalid-name
_web_interface_ws_connections = {} # pylint: disable=invalid-name

# TODO: Make this an instance variable in handle_websocket
_mobile_interface_ws_connections = {} # pylint: disable=invalid-name


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

    _websocket_metadata = {}

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

            _ws_routes[message_type](decoded_message, websocket,
                                     _websocket_metadata)
        except WebSocketError:
            break

    #_web_interface_ws_connections.remove(websocket)
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

    # There's probably a better way to do this and it should be refactored
    for attribute, value in message.items():
        metadata[attribute] = value

    # Dead code, to be removed
    #_mobile_interface_ws_connections[websocket] = message['apiKey']
    #print(_mobile_interface_ws_connections)

@ws_router('logDump')
def log_dump(message, websocket, metadata):
    """ Handles Log Dumps from the Mobile API

    When a log dump comes in from the Mobile API, this function takes the raw
    log data, parses it and sends the parsed data to all connected web clients.

    Args:
        message: the decoded JSON message from the Mobile API
        websocket: the full websocket connection
    """
    parsed_logs = LogParser.parse(message)

    api_key = metadata["apiKey"]

    # Dead code
    #api_key = _mobile_interface_ws_connections[websocket]

    # At first glance this looks like a copy, 
    # but this is actually grabbing the keys from a dict
    web_ws_connections = [ws for ws in _web_interface_ws_connections]
    associated_websockets = ( 
        controller.user_management_interface.find_associated_websockets(api_key,
            web_ws_connections))

    for connection in associated_websockets:
        connection.send(util.serialize_json(parsed_logs))

@ws_router('endSession')
def end_session(message, websocket, metadata):
    print("currently defunct")
    # This function may become meaningless in the context of just streaming logs
    # TODO: Remove websocket from list of websockets
    #del _mobile_interface_ws_connections[websocket]

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
    """ Classic graveyarded code
    connection = {
        'api_key': message['apiKey'],
        'websocket': websocket,
    }
    _web_interface_ws_connections.append(connection)
    """
    _web_interface_ws_connections[websocket] = message['apiKey']
