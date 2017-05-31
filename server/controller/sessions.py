"""
Session Controller
"""

from bottle import get, post
import controller

@get('/sessionList')
def getSessionList():
    return {}

@get('/deviceList')
def getDeviceList():
    return controller._datastore_interface.retrieve_devices_and_apps(controller._current_guid)

@post('/appList')
def postAppList():
    return{}
