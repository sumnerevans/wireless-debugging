"""
Tests the base datastore interface class. 
This is an abstract class so it just verifies everything is unimplemented

These tests are pretty trivial.
"""

import pytest

from datastore_interfaces import base_datastore_interface
from bottle import request, response
import datetime

def test_store_logs():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_name = "Hangouts"
    start_time = str(datetime.datetime.now())
    os_type = "Android"
    log_entries = {}
    with pytest.raises(NotImplementedError):
        di.store_logs(api_key, device_name, app_name, start_time, os_type, log_entries)

def test_set_session_over():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_name = "Hangouts"
    start_time = str(datetime.datetime.now())
    with pytest.raises(NotImplementedError):
        di.set_session_over(api_key, device_name, app_name, start_time)

def test_retrieve_logs():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_name = "Hangouts"
    start_time = str(datetime.datetime.now())
    with pytest.raises(NotImplementedError):
        di.retrieve_logs(api_key, device_name, app_name, start_time)
        
def test_retrieve_devices():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    with pytest.raises(NotImplementedError):
        di.retrieve_devices(api_key)

def test_retrieve_apps():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    with pytest.raises(NotImplementedError):
        di.retrieve_apps(api_key, device_name)

def test_retrieve_sessions():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_name = "Hangouts"
    with pytest.raises(NotImplementedError):
        di.retrieve_sessions(api_key, device_name, app_name)

def test_add_device_app():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_name = "Hangouts"
    with pytest.raises(NotImplementedError):
        di.add_device_app(api_key, device_name, app_name)

def test_alias_device():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_raw_name = "Pixel"
    device_alias = "Pixel2"
    with pytest.raises(NotImplementedError):
        di.alias_device(api_key, device_raw_name, device_alias)

def test_alias_app():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_raw_name = "Hangouts"
    app_alias = "Hangouts2"
    with pytest.raises(NotImplementedError):
        di.alias_app(api_key, device_name, app_raw_name, app_alias)

def test_get_raw_device_name_from_alias():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_alias = "Pixel"
    with pytest.raises(NotImplementedError):
        di.get_raw_device_name_from_alias(api_key, device_alias)

def test_get_raw_app_name_from_alias():
    """Checks if the function is not implemented"""
    di = base_datastore_interface.DatastoreInterface()
    api_key = "23"
    device_name = "Pixel"
    app_alias = "Hangouts2"
    with pytest.raises(NotImplementedError):
        di.get_raw_app_name_from_alias(api_key, device_name, app_alias)

