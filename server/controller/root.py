"""
Root Controller
"""

from bottle import route


@route('/')
def index():
    return 'Hello World'
