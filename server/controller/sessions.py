"""
Session Controller
"""

from bottle import get, post, request
import controller

@get('/sessionList')
def getSessionList():
    return {}

@get('/deviceList')
def getDeviceList():
    return {"devices": controller._datastore_interface.retrieve_devices(controller._current_guid)}

@post('/appList')
def postAppList():
    return {"apps":controller._datastore_interface.retrieve_apps(controller._current_guid, request.json['device'])}
