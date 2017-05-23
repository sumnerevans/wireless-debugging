"""
WebSocket Controller
"""

import json

from bottle import route, request, abort

from geventwebsocket import WebSocketError

# Store a dictionary of string -> function
_ws_routes = {}

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

            _ws_routes[messageType](decoded_message)
        except WebSocketError:
            break

# Provide a decorator for adding functions to the _ws_route dictionary
def ws_router(messageType):
    def decorator(function):
        _ws_routes[messageType] = function

    return decorator

@ws_router('logDump')
def logDump(message):
    print('Log Dump: %s' % message)


@ws_router('associateSession')
def associateSession(message):
    print('Log Dump: %s' % message)
