from pymongo import MongoClient
from pprint import pprint

from datastore_interfaces.base_datastore_interface import DatastoreInterface

class MongoDatastoreInterface(DatastoreInterface):
    def __init__(self, hostname=None):
        """ Set up datastore interface
        Ensure MongoDB is installed with the default location.
        Ensure pymongo is installed.
        Ensure that you run `mongod` before executing the application.
        Args:
            hostname : hostname. Defaulted to None
        """
        self._client = MongoClient()
        self._db = self._client.test_database
        self._logs = self._db.logs
        self._dev = self._db.dev
        self._app = self._db.app
        self._sessions = self._db.sessions

    def store_logs(self, api_key, device_name, app_name, start_time, os_type, log_entries):
        """Store a set of log entries to the datastore. This function may be called multiple times per session, so it must append the log entries in the storage mechanism.
        Args
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started
            os_type: the OS type (iOS or Android)
            log_entries: the log entries to store
        """
        self._logs.insert( { "api_key": api_key, "device_name": device_name, "app_name": app_name, "start_time": start_time, "os_type": os_type, "log_entries": log_entries, "ended" : False } )

    def set_session_over(self, api_key, device_name, app_name, start_time):
        """Called to indicate to the datastore that the session is over. This can set a flag on the session in the datastore indicating that it should not be modified, for example.
        Args:
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started
        """
        session = self._logs.find_one({"api_key": api_key, "device_name": device_name, "app_name": app_name, "start_time": start_time })
        if session is not None:
            session['ended'] = True
            self._logs.save(session)

    def retrieve_logs(self, api_key, device_name, app_name, start_time):
        """Retrieve logs for given session
        Args:
            api_key: the API Key to retrieve logs for
            device_name: the name of the device to retrieve logs for
            app_name: the name of the app to retrieve logs for
            start_time: the time that the session started
        Returns:
            osType: the OS type
            logEntries: a list of log entries as Python dictionaries
        """
        return self._logs.distinct("log_entries", {"api_key": api_key, "device_name": self.get_raw_device_name_from_alias(api_key, device_name), "app_name": self.get_raw_app_name_from_alias(api_key, device_name, app_name), "start_time": start_time})[0]['logEntries']
    
    def retrieve_devices(self, api_key):
        """Retrieve a list of devices associated with the given API Key
        Args:
            api_key: the API Key to retrieve devices for
        Returns:
            array: array of names of device names
        """
        return self._dev.distinct("alias", {"api_key" : api_key})

    def retrieve_apps(self, api_key, device_name):
        """Retrieves apps given a device
        Args:
            api_key: the API Key to retrieve logs for
            device_name: the device name to retrieve logs for
        Returns:
            array: array of the names of the apps on the given device
        """
        return self._app.distinct("alias", {"api_key": api_key, "device_name": self.get_raw_device_name_from_alias(api_key, device_name)})

    def retrieve_sessions(self, api_key, device_name, app_name):
        """Retrieve a list of sessions for a given API Key, device, and app.
        Args:
            api_key: the API Key to retrieve sessions for
            device_name: the name of the device to retrieve sessions for
            app_name: the name of the app to retrieve sessions for
        Returns:
            array: list of datetime objects, one for each of the session start times associated with the given API Key, device, and app
        """
        return self._logs.distinct("start_time", {"api_key": api_key, "device_name": self.get_raw_device_name_from_alias(api_key, device_name), "app_name": self.get_raw_app_name_from_alias(api_key, device_name, app_name), "ended": True})

    def add_device_app(self, api_key, device_name, app_name):
        """Add a device/app combination to the device/app collection
        Args:
            api_key: the API Key
            device_name: api_key contatenated with the name of the device
            app_name: the name of the app
        """
        dev = self._dev.find_one({"api_key": api_key, "device_name": device_name})
        if dev is None:
            print ("here")
            self._dev.insert( { "api_key": api_key, "device_name": device_name, "alias": device_name } )
        app = self._app.find_one({"api_key": api_key, "app_name": app_name})
        if app is None:
            self._app.insert( { "api_key": api_key, "device_name": device_name, "app_name": app_name, "alias": app_name } )

    def alias_device(self, api_key, device_raw_name, device_alias):
        """Updates alias for a device
        Args:
            api_key: the API key
            device_raw_name: name being aliased
            device_alias: new alias for device
        """
        dev = self._dev.find_one({"api_key": api_key, "device_name": self.get_raw_device_name_from_alias(api_key, device_raw_name)})
        if dev is not None:
            dev['alias'] = device_alias
            self._dev.save(dev)

    def alias_app(self, api_key, device_name, app_raw_name, app_alias):
        """Updates alias for an app
        Args:
            api_key: the API key
            device_name: device connected to app
            app_raw_name: name being aliased 
            app_alias: new alias for app
        """
        app = self._app.find_one({"api_key": api_key, "app_name": self.get_raw_app_name_from_alias(api_key, device_name, app_raw_name)})
        if app is not None:
            app['alias'] = app_alias
            self._app.save(app)

    def get_raw_device_name_from_alias(self, api_key, device_alias):
        """Returns the raw device name based on an alias
        Args:
            api_key: the API key
            device_alias: alias
        Returns:
            string: raw device name 
        """
        return self._dev.find_one({"api_key" : api_key, "alias": device_alias})['device_name'].strip()

    def get_raw_app_name_from_alias(self, api_key, device_name, app_alias):
        """Returns raw app name based on an alias
        Args:
            api_key: the API key
            device_name: device connected to app
            app_alias: alias for app
        Returns:
            string: raw app name
        """
        return self._app.find_one({"api_key": api_key, "device_name": self.get_raw_device_name_from_alias(api_key, device_name), "alias": app_alias})['app_name'].strip()
