"""
Session Controller
"""
from helpers.config_manager import ConfigManager

from bottle import request, route
from parsing_lib.log_parser import LogParser


@route('/deviceList')
def get_device_list():
    """ This function retrieves the list of devices for a given api_key."""
    api_key = request.query.get('apiKey').strip()
    devices = ConfigManager.datastore_interface.retrieve_devices(api_key)
    return {
        'success': devices != [],
        'devices': devices,
    }


@route('/appList')
def get_app_list():
    """ This function retrieves the list of apps for a given api_key and device."""
    api_key = request.query.get('apiKey').strip()
    device = request.query.get('device').strip()
    return {
        'apps': ConfigManager.datastore_interface.retrieve_apps(
            api_key, device)
    }


@route('/sessionList')
def get_session_list():
    """ This function retrieves the list of start times for a given api_key, device, and app."""
    api_key = request.query.get('apiKey').strip()
    device = request.query.get('device').strip()
    app = request.query.get('app').strip()
    return {
        'starttimes':
        ConfigManager.datastore_interface.retrieve_sessions(
            api_key, device, app)
    }


@route('/logs')
def get_logs():
    """ This function retrieves the logs for a given api_key, device, app, and start time."""
    api_key = request.query.get('apiKey').strip()
    device = request.query.get('device').strip()
    app = request.query.get('app').strip()
    start_time = request.query.get('starttime').strip()
    return {
        'logs':
        LogParser.convert_to_html(
            ConfigManager.datastore_interface.retrieve_logs(
                api_key, device, app, start_time))
    }


@route('/aliasDevice')
def post_alias_device():
    """ This function stores an alias for a device given the device name."""
    api_key = request.query.get('apiKey').strip()
    device = request.query.get('device').strip()
    dev_alias = request.query.get('alias').strip()
    dev_success = ConfigManager.datastore_interface.update_alias_device(
        api_key, device, dev_alias)
    return {'dev_success': dev_success}


@route('/aliasApp')
def post_alias_app():
    """ This function stores an alias for an app given the app's name."""
    api_key = request.query.get('apiKey').strip()
    device = request.query.get('device').strip()
    app = request.query.get('app').strip()
    app_alias = request.query.get('alias').strip()
    app_success = ConfigManager.datastore_interface.update_alias_app(
        api_key, device, app, app_alias)
    return {'app_success': app_success}


@route('/clearDatastore')
def get_clear_datastore():
    """ This function clears the datastore of any entries. """
    ConfigManager.datastore_interface.clear_datastore()
