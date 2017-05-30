# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Session Controller
"""

from bottle import get


@get('/sessionList')
def getSessionList():
    return {}
