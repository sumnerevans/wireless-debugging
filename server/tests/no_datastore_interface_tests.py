"""
Tests the no datastore interface class
These tests verify mostly nothing is returned from the class.

These tests are pretty trivial.
"""

from datastore_interfaces import no_datastore_interface

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
            "\tat com.google.wireless.debugging.example.MainFragment$2.",
            "onClick(MainFragment.java:73)",
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
    """This function checks if store_logs returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.store_logs(api_key, device_name, app_name, start_time, os_type,
                         log_entries) is None


def test_set_session_over():
    """This function checks if set_session_over returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.set_session_over(
        api_key, device_name, app_name, start_time) is None


def test_retrieve_logs():
    """This function checks if retrieve_logs returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.retrieve_logs(api_key, device_name, app_name, start_time) is None


def test_retrieve_devices():
    """This function checks if retrieve_devices returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.retrieve_devices(api_key) == []


def test_retrieve_apps():
    """This function checks if retrieve_apps returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.retrieve_apps(api_key, device_name) == []


def test_retrieve_sessions():
    """This function checks if retrieve_sessions returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.retrieve_sessions(api_key, device_name, app_name) == []


def test_add_device_app():
    """This function checks if add_device_app returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.add_device_app(api_key, device_name, app_name) is None


def test_update_device_alias():
    """This function checks if update_device_alias returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.update_device_alias(api_key, device_name, "Alias") is None


def test_update_app_alias():
    """This function checks if update_app_alias returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.update_app_alias(api_key, device_name, app_name, "Alias") is None


def test_get_raw_device_name_from_alias():
    """This function checks if get_raw_device_name_from_alias returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.get_raw_device_name_from_alias(api_key, "Alias") == ''


def test_get_raw_app_name_from_alias():
    """This function checks if get_raw_name_from_alias returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.get_raw_app_name_from_alias(api_key, device_name, "Alias") == ''


def test_clear_datastore():
    """This function checks if clear_datastore returns nothing."""
    di = no_datastore_interface.NoDatastoreInterface()
    assert di.clear_datastore() is None
