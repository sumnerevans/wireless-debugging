# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Session Controller
"""

from bottle import get, post, request
import controller
from parsing_lib.log_parser import LogParser

@post('/sessionList')
def postSessionList():
    return {"starttimes": controller._datastore_interface.retrieve_sessions(request.json['apiKey'].strip(), request.json['device'], request.json['app'])}

@post('/deviceList')
def postDeviceList():
    return {"devices": controller._datastore_interface.retrieve_devices(request.json['apiKey'].strip())}

@post('/appList')
def postAppList():
    return {"apps":controller._datastore_interface.retrieve_apps(request.json['apiKey'].strip(), request.json['device'])}

@post('/logs')
def getLogs():
    return {"logs": LogParser.convert_to_html(controller._datastore_interface.retrieve_logs(request.json['apiKey'].strip(), request.json['device'], request.json['app'], request.json['starttime']))}

@post('/aliasDevice')
def postAliasDevice():
    controller._datastore_interface.alias_device(request.json['apiKey'].strip(), request.json['device'], request.json['alias'])
    return {}

@post('/aliasApp')
def postAliasApp():
    controller._datastore_interface.alias_app(request.json['apiKey'].strip(), request.json['device'], request.json['app'], request.json['alias'])
    return {}
