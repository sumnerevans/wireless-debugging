"""
Session Controller
"""

from bottle import get

@get('/sessionList')
def getSessionList():
    return {}
