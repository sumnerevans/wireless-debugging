"""
Tests the mongo datastore interface class.
"""

import pytest

from datastore_interfaces import mongo_datastore_interface

api_key = "23"
device_name = "Pixel"
app_name = "Hangouts"
start_time = "2017-06-06 22:32:42.783083"
os_type = "Android"
log_entries = {
    "messageType": "logData",
    "osType": "Android",
    "logEntries": [{
        "time": "05-24 12:12:49.247000",
        "logType": "Error",
        "tag": "AndroidRuntime",
        "text": [
            "FATAL EXCEPTION: main",
            "Process: com.google.wireless.debugging, PID: 23930",
            "java.lang.RuntimeException: Forced Crash",
            "\tat com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)",
            "\tat android.view.View.performClick(View.java:4445)",
            "\tat android.view.View$PerformClick.run(View.java:18446)",
            "\tat android.os.Handler.handleCallback(Handler.java:733)",
            "\tat android.os.Handler.dispatchMessage(Handler.java:95)",
            "\tat android.os.Looper.loop(Looper.java:136)",
            "\tat android.app.ActivityThread.main(ActivityThread.java:5146)",
            "\tat java.lang.reflect.Method.invokeNative(Native Method)",
            "\tat java.lang.reflect.Method.invoke(Method.java:515)",
            "\tat com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)",
            "\tat com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)",
            "\tat dalvik.system.NativeStart.main(Native Method)"
        ]
    }]
}

logs = [{
    "time": "05-24 12:12:49.247000",
    "logType": "Error",
    "tag": "AndroidRuntime",
    "text": [
        "FATAL EXCEPTION: main",
        "Process: com.google.wireless.debugging, PID: 23930",
        "java.lang.RuntimeException: Forced Crash",
        "\tat com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)",
        "\tat android.view.View.performClick(View.java:4445)",
        "\tat android.view.View$PerformClick.run(View.java:18446)",
        "\tat android.os.Handler.handleCallback(Handler.java:733)",
        "\tat android.os.Handler.dispatchMessage(Handler.java:95)",
        "\tat android.os.Looper.loop(Looper.java:136)",
        "\tat android.app.ActivityThread.main(ActivityThread.java:5146)",
        "\tat java.lang.reflect.Method.invokeNative(Native Method)",
        "\tat java.lang.reflect.Method.invoke(Method.java:515)",
        "\tat com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)",
        "\tat com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)",
        "\tat dalvik.system.NativeStart.main(Native Method)"
    ]
}]


def test_store_logs():
    """This function checks if class stores session information as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.store_logs(api_key, device_name, app_name,
                  start_time, os_type, log_entries)
    log = di._logs.find_one()
    assert log['api_key'] == api_key
    assert log['device_name'] == device_name
    assert log['app_name'] == app_name
    assert log['start_time'] == start_time
    assert log['os_type'] == os_type
    assert log['log_entries'] == log_entries
    assert not log['ended']
    di.clear_datastore()


def test_set_session_over():
    """This function checks if class sets session over as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.store_logs(api_key, device_name, app_name,
                  start_time, os_type, log_entries)
    di.set_session_over(api_key, device_name, app_name, start_time)
    log = di._logs.find_one()
    assert log['api_key'] == api_key
    assert log['device_name'] == device_name
    assert log['app_name'] == app_name
    assert log['start_time'] == start_time
    assert log['os_type'] == os_type
    assert log['log_entries'] == log_entries
    assert log['ended']
    di.clear_datastore()


def test_retrieve_logs():
    """This function checks if class retrieves logs as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.store_logs(api_key, device_name, app_name, start_time, os_type,
                  log_entries)
    di.add_device_app(api_key, device_name, app_name)
    log = di.retrieve_logs(api_key, device_name, app_name, start_time)
    assert log == logs
    di.clear_datastore()


def test_retrieve_devices():
    """This function checks if class retrieves device list as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    devices = di.retrieve_devices(api_key)
    assert devices == ['Pixel']
    di.clear_datastore()


def test_retrieve_apps():
    """This function checks if class retrieves app list as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    apps = di.retrieve_apps(api_key, device_name)
    assert apps == ['Hangouts']
    di.clear_datastore()


def test_retrieve_sessions():
    """This function checks if class retrieves start_times as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    di.store_logs(api_key, device_name, app_name,
                  start_time, os_type, log_entries)
    di.set_session_over(api_key, device_name, app_name, start_time)
    session = di.retrieve_sessions(api_key, device_name, app_name)
    assert session == [start_time]
    di.clear_datastore()


def test_add_device_app():
    """This function checks if class adds device/app to historical databases as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    log_dev = di._device.find_one()
    assert log_dev['api_key'] == api_key
    assert log_dev['device_name'] == device_name
    assert log_dev['device_alias'] == device_name
    log_app = di._app_name.find_one()
    assert log_app['app_name'] == app_name
    assert log_app['api_key'] == api_key
    assert log_app['device_name'] == device_name
    assert log_app['app_alias'] == app_name
    di.clear_datastore()


def test_update_alias_device():
    """This function checks if class aliases device as expected including ensuring uniqueness."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    assert di.update_alias_device(api_key, device_name, "Alias")
    log_dev = di._device.find_one()
    assert log_dev['api_key'] == api_key
    assert log_dev['device_name'] == device_name
    assert log_dev['device_alias'] == "Alias"
    di.add_device_app("23", "dev", "app")
    assert not di.update_alias_device("23", "dev", "Alias")
    di.clear_datastore()


def test_update_alias_app():
    """This function checks if class aliases apps expected including ensuring uniqueness."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    assert di.update_alias_app(api_key, device_name, app_name, "Alias")
    log_app = di._app_name.find_one()
    assert log_app['api_key'] == api_key
    assert log_app['device_name'] == device_name
    assert log_app['app_name'] == app_name
    assert log_app['app_alias'] == "Alias"
    di.add_device_app("23", "dev", "app")
    assert not di.update_alias_app("23", "dev", "app", "Alias")
    di.clear_datastore()


def test_get_raw_device_name_from_alias():
    """This function checks if class retrieves raw device name given an alias as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    di.update_alias_device(api_key, device_name, "Alias")
    raw_dev_name = di.get_raw_device_name_from_alias(api_key, "Alias")
    assert raw_dev_name == device_name
    di.clear_datastore()


def test_get_raw_app_name_from_alias():
    """This function checks if class retrieves raw app name given an alias as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.add_device_app(api_key, device_name, app_name)
    di.update_alias_app(api_key, device_name, app_name, "Alias")
    raw_app_name = di.get_raw_app_name_from_alias(
        api_key, device_name, "Alias")
    assert raw_app_name == app_name
    di.clear_datastore()


def test_clear_datastore():
    """This function checks if class clears datastore of data as expected."""
    di = mongo_datastore_interface.MongoDatastoreInterface("testing_database")
    di.clear_datastore()
    assert di._logs.find_one() is None
    assert di._app_name.find_one() is None
    assert di._device.find_one() is None
    assert di._start_times.find_one() is None
