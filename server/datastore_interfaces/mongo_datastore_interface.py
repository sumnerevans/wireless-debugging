from pymongo import MongoClient

from datastore_interfaces.base_datastore_interface import DatastoreInterface


class MongoDatastoreInterface(DatastoreInterface):
    """This is the Mongo Datastore interface implementing the base interface."""

    def __init__(self, hostname="test_database"):
        """ This function sets up datastore interface.
        Ensure MongoDB is installed with the default location.
        Ensure pymongo is installed.
        Ensure that you run `mongod` before executing the application.

        Args:
            hostname : hostname. Defaulted to test_database
        """
        self._client = MongoClient()
        self._db = self._client[hostname]
        self._logs = self._db.logs
        self._dev = self._db.dev
        self._app = self._db.app
        self._sessions = self._db.sessions

    def store_logs(self, api_key, device_name, app_name, start_time, os_type, log_entries):
        """This function stores a set of log entries to the datastore. This function may
           be called multiple times per session, so it must append the log entries in
           the storage mechanism.

        Args
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started
            os_type: the OS type (iOS or Android)
            log_entries: the log entries to store
        """
        self._logs.insert_one({"api_key": api_key, "device_name": device_name, "app_name": app_name,
                               "start_time": start_time, "os_type": os_type,
                               "log_entries": log_entries, "ended": False})

    def set_session_over(self, api_key, device_name, app_name, start_time):
        """This function is called to indicate to the datastore that the session is over.
           This can set a flag on the session in the datastore indicating that it
           should not be modified, for example.

        Args:
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started
        """
        session = self._logs.find_one(
            {"api_key": api_key, "device_name": device_name,
             "app_name": app_name, "start_time": start_time})
        if session is not None:
            session['ended'] = True
            self._logs.update_one({"api_key": api_key, "device_name": device_name,
                                   "app_name": app_name, "start_time": start_time},
                                  {"$set": session}, upsert=False)

    def retrieve_logs(self, api_key, device_name, app_name, start_time):
        """This function retrieves logs for the given session.

        Args:
            api_key: the API Key to retrieve logs for
            device_name: the name of the device to retrieve logs for
            app_name: the name of the app to retrieve logs for
            start_time: the time that the session started

        Returns:
            osType: the OS type
            logEntries: a list of log entries as Python dictionaries
        """
        return self._logs.distinct("log_entries",
                                   {"api_key": api_key,
                                    "device_name":
                                        self.get_raw_device_name_from_alias(
                                            api_key, device_name),
                                    "app_name":
                                        self.get_raw_app_name_from_alias(
                                            api_key, device_name, app_name),
                                    "start_time": start_time})[0]['logEntries']

    def retrieve_devices(self, api_key):
        """This function retrieves a list of devices associated with the given API Key.

        Args:
            api_key: the API Key to retrieve devices for

        Returns:
            array: array of names of device names
        """
        return self._dev.distinct("device_alias", {"api_key": api_key})

    def retrieve_apps(self, api_key, device_name):
        """This function retrieves apps given a device.

        Args:
            api_key: the API Key to retrieve logs for
            device_name: the device name to retrieve logs for

        Returns:
            array: array of the names of the apps on the given device
        """
        return self._app.distinct("app_alias",
                                  {"api_key": api_key,
                                   "device_name":
                                   self.get_raw_device_name_from_alias(
                                       api_key, device_name),
                                  })

    def retrieve_sessions(self, api_key, device_name, app_name):
        """This function retrieves a list of sessions for a given API Key, device, and app.

        Args:
            api_key: the API Key to retrieve sessions for
            device_name: the name of the device to retrieve sessions for
            app_name: the name of the app to retrieve sessions for

        Returns:
            array: list of datetime objects, one for each of the session start
                   times associated with the given API Key, device, and app
        """
        return self._logs.distinct("start_time",
                                   {"api_key": api_key,
                                    "device_name":
                                        self.get_raw_device_name_from_alias(
                                            api_key, device_name),
                                    "app_name":
                                        self.get_raw_app_name_from_alias(
                                            api_key, device_name, app_name),
                                    "ended": True})

    def add_device_app(self, api_key, device_name, app_name):
        """This function adds a device/app combination to the device/app collection.

        Args:
            api_key: the API Key
            device_name: the name of the device
            app_name: the name of the app
        """
        dev = self._dev.find_one(
            {"api_key": api_key, "device_name": device_name})
        if dev is None:
            self._dev.insert_one(
                {"api_key": api_key, "device_name": device_name, "device_alias": device_name})
        app = self._app.find_one(
            {"api_key": api_key, "device_name": device_name, "app_name": app_name})
        if app is None:
            self._app.insert_one({"api_key": api_key, "device_name": device_name,
                                  "app_name": app_name, "app_alias": app_name})

    def alias_device(self, api_key, device_raw_name, device_alias):
        """This function updates alias for a device.

        Args:
            api_key: the API key
            device_raw_name: name being aliased
            device_alias: new alias for device
        """
        find_dev_alias = self._dev.find_one(
            {"api_key": api_key, "device_alias": device_alias})
        if find_dev_alias is None:
            dev = self._dev.find_one(
                {"api_key": api_key,
                 "device_name": self.get_raw_device_name_from_alias(api_key, device_raw_name)})
            if dev is not None:
                dev['device_alias'] = device_alias
                self._dev.update_one(
                    {"api_key": api_key,
                     "device_name": self.get_raw_device_name_from_alias(api_key, device_raw_name)},
                    {"$set": dev}, upsert=False)
            return True
        else:
            return False

    def alias_app(self, api_key, device_name, app_raw_name, app_alias):
        """This function updates alias for an app.

        Args:
            api_key: the API key
            device_name: device connected to app
            app_raw_name: name being aliased
            app_alias: new alias for app
        """
        find_app_alias = self._app.find_one(
            {"api_key": api_key, "app_alias": app_alias})
        if find_app_alias is None:
            app = self._app.find_one(
                {"api_key": api_key, "app_name": self.get_raw_app_name_from_alias(
                    api_key, device_name, app_raw_name)})
            if app is not None:
                app['app_alias'] = app_alias
                self._app.update_one(
                    {"api_key": api_key, "app_name": self.get_raw_app_name_from_alias(
                        api_key, device_name, app_raw_name)},
                    {"$set": app}, upsert=False)
            return True
        else:
            return False

    def get_raw_device_name_from_alias(self, api_key, device_alias):
        """This function returns the raw device name based on an alias.

        Args:
            api_key: the API key
            device_alias: alias

        Returns:
            string: raw device name
        """
        return self._dev.find_one(
            {"api_key": api_key,
             "device_alias": device_alias})['device_name'].strip()

    def get_raw_app_name_from_alias(self, api_key, device_name, app_alias):
        """This function returns raw app name based on an alias.

        Args:
            api_key: the API key
            device_name: device connected to app
            app_alias: alias for app

        Returns:
            string: raw app name
        """
        return self._app.find_one(
            {"api_key": api_key,
             "device_name": self.get_raw_device_name_from_alias(api_key, device_name),
             "app_alias": app_alias})['app_name'].strip()

    def clear_datastore(self):
        """This function clears datastore of records."""
        self._logs.drop()
        self._dev.drop()
        self._app.drop()
        self._sessions.drop()
