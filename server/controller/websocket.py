"""
WebSocket Controller
"""

import json
import time

from bottle import route, request, abort

from geventwebsocket import WebSocketError

# Store a dictionary of string -> function
_ws_routes = {}
_web_interface_ws_connections = []


@route('/ws')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            decoded_message = json.loads(message)
            messageType = decoded_message['messageType']
            if messageType is None:
                # TODO: blow up
                pass

            _ws_routes[messageType](decoded_message, wsock)
        except WebSocketError:
            break


def ws_router(messageType):
    """Provide a decorator for adding functions to the _ws_route dictionary"""
    def decorator(function):
        _ws_routes[messageType] = function

    return decorator


@ws_router('logDump')
def logDump(message, wsock):
    # TODO: This function is entirely a placeholder for testing purposes
    parsed_logs = json.dumps({
        'messageType': 'logData',
        'osType': 'Android',
        'logEntries': [
            {
                'time': '2017-11-06T16:34:41.000Z',
                'text': 'This is not a real error',
                'tag': 'TEST',
                'logType': 'Warning',
            },
            {
                'time': '2017-11-06T16:34:50.000Z',
                'text': 'Cool Log',
                'tag': 'TEST',
                'logType': 'Info',
            },
        ]
    })

    for c in _web_interface_ws_connections:
        c.send(parsed_logs)
        time.sleep(1)
        c.send(parsed_logs)


@ws_router('associateSession')
def associateSession(message, wsock):
    """
    Associate a WebSocket connection with a session.
    """
    _web_interface_ws_connections.append(wsock)
