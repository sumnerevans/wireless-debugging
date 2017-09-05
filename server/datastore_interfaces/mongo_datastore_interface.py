from pymongo import MongoClient
from datastore_interfaces import base_datastore_interface


class MongoDatastoreInterface(base_datastore_interface.DatastoreInterface):
    """This is the Mongo Datastore interface implementing the base interface."""

    def __init__(self, hostname='wireless_debugging'):
        """ Set up the Datastore by connecting to the MongoDB instance.

        Args:
            hostname: the MongoDB hostname to connect to. Defaulted to
            wireless_debugging.
        """
        super().__init__()
        self._client = MongoClient()
        self._logs = self._client[hostname].logs
        self._device = self._client[hostname].dev
        self._app_name = self._client[hostname].app
        self._start_times = self._client[hostname].sessions

    def store_logs(self, api_key, device_name, app_name, start_time, os_type,
                   log_entries):
        """ Stores a set of log entries to the datastore. This function may be
        called multiple times per session, so it must append the log entries in
        the storage mechanism.

        Args
            api_key:     the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name:    the name of the app associated with the logs
            start_time:  the time that the session started
            os_type:     the OS type (iOS or Android)
            log_entries: the log entries to store
        """
        self._logs.insert_one({
            'api_key': api_key,
            'device_name': device_name,
            'app_name': app_name,
            'start_time': start_time,
            'os_type': os_type,
            'log_entries': log_entries,
            'ended': False,
        })

    def set_session_over(self, api_key, device_name, app_name, start_time):
        """ Called to indicate to the datastore that the session is over.  This
        sets the "ended" flag to true on the session.

        Args:
            api_key:     the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name:    the name of the app associated with the logs
            start_time:  the time that the session started
        """
        self._logs.update_one(
            {
                'api_key': api_key,
                'device_name': device_name,
                'app_name': app_name,
                'start_time': start_time,
            }, {'$set': {
                'ended': True,
            }},
            upsert=True)

    def retrieve_logs(self, api_key, device_name, app_name, start_time):
        """ Retrieves logs for the given session.

        Args:
            api_key:     the API Key to retrieve logs for
            device_name: the name of the device to retrieve logs for
            app_name:    the name of the app to retrieve logs for
            start_time:  the time that the session started

        Returns:
            osType:     the OS type
            logEntries: a list of log entries as Python dictionaries
        """
        raw_dev_name = self.get_raw_device_name_from_alias(api_key, device_name)
        raw_app_name = self.get_raw_app_name_from_alias(api_key, device_name,
                                                        app_name)
        return self._logs.distinct('log_entries', {
            'api_key': api_key,
            'device_name': raw_dev_name,
            'app_name': raw_app_name,
            'start_time': start_time,
        })

    def retrieve_devices(self, api_key):
        """ Retrieves a list of devices associated with the given API Key.

        Args:
            api_key: the API Key to retrieve devices for

        Returns:
            array: array of names of device names
        """
        return self._device.distinct('device_alias', {'api_key': api_key})

    def retrieve_apps(self, api_key, device_name):
        """ Retrieves apps for the given device.

        Args:
            api_key:     the API Key to retrieve logs for
            device_name: the device name to retrieve logs for

        Returns:
            array: array of the names of the apps on the given device
        """
        raw_dev_name = self.get_raw_device_name_from_alias(api_key, device_name)
        return self._app_name.distinct('app_alias', {
            'api_key': api_key,
            'device_name': raw_dev_name,
        })

    def retrieve_sessions(self, api_key, device_name, app_name):
        """ Retrieves a list of sessions for a given API Key, device, and app.

        Args:
            api_key:     the API Key to retrieve sessions for
            device_name: the name of the device to retrieve sessions for
            app_name:    the name of the app to retrieve sessions for

        Returns:
            array: list of datetime objects, one for each of the session start
                   times associated with the given API Key, device, and app
        """
        device_name = self.get_raw_device_name_from_alias(api_key, device_name)
        app_name = self.get_raw_app_name_from_alias(api_key, device_name,
                                                    app_name)
        return self._logs.distinct('start_time', {
            'api_key': api_key,
            'device_name': device_name,
            'app_name': app_name,
            'ended': True,
        })

    def add_device_app(self, api_key, device_name, app_name):
        """ Adds a device/app combination to the device/app collection.

        Args:
            api_key:     the API Key
            device_name: the name of the device
            app_name:    the name of the app
        """
        find_device = self._device.find_one({
            'api_key': api_key,
            'device_name': device_name,
        })
        if not find_device:
            self._device.insert_one({
                'api_key': api_key,
                'device_name': device_name,
                'device_alias': device_name,
            })

        find_app = self._app_name.find_one({
            'api_key': api_key,
            'device_name': device_name,
            'app_name': app_name,
        })
        if not find_app:
            self._app_name.insert_one({
                'api_key': api_key,
                'device_name': device_name,
                'app_name': app_name,
                'app_alias': app_name,
            })

    def update_device_alias(self, api_key, device_raw_name, device_alias):
        """ Updates the alias for a device.

        Args:
            api_key:         the API key
            device_raw_name: name being aliased
            device_alias:    new alias for device. This is what shows in the web app dropboxes.
        """
        device_name = self.get_raw_device_name_from_alias(
            api_key, device_raw_name)
        find_dev_alias = self._device.find_one({
            'api_key': api_key,
            'device_alias': device_alias,
        })
        if find_dev_alias:
            return False

        find_device = self._device.find_one({
            'api_key': api_key,
            'device_name': device_name,
        })
        if find_device:
            find_device['device_alias'] = device_alias
            self._device.update_one(
                {
                    'api_key': api_key,
                    'device_name': device_name,
                }, {'$set': find_device},
                upsert=True)
        return True

    def update_app_alias(self, api_key, device_name, app_raw_name, app_alias):
        """ Updates the alias for an app.

        Args:
            api_key:      the API key
            device_name:  device connected to app
            app_raw_name: name being aliased
            app_alias:    new alias for app. This is what shows in the web app dropboxes.
        """
        find_app_alias = self._app_name.find_one({
            'api_key': api_key,
            'app_alias': app_alias,
        })
        if find_app_alias:
            return False

        app = self._app_name.find_one({
            'api_key':
            api_key,
            'app_name':
            self.get_raw_app_name_from_alias(api_key, device_name,
                                             app_raw_name),
        })
        if app:
            app['app_alias'] = app_alias
            self._app_name.update_one(
                {
                    'api_key':
                    api_key,
                    'app_name':
                    self.get_raw_app_name_from_alias(api_key, device_name,
                                                     app_raw_name),
                }, {'$set': app},
                upsert=True)
        return True

    def get_raw_device_name_from_alias(self, api_key, device_alias):
        """This function returns the raw device name based on an alias.

        Args:
            api_key: the API key
            device_alias: alias

        Returns:
            string: raw device name
        """
        device_alias_entry = self._device.find_one({
            'api_key': api_key,
            'device_alias': device_alias,
        })

        # Returns the device_name associated with an alias.
        return device_alias_entry['device_name'].strip()

    def get_raw_app_name_from_alias(self, api_key, device_name, app_alias):
        """This function returns raw app name based on an alias.

        Args:
            api_key: the API key
            device_name: device connected to app
            app_alias: alias for app

        Returns:
            string: raw app name
        """
        device_name = self.get_raw_device_name_from_alias(api_key, device_name)
        return self._app_name.find_one({
            'api_key': api_key,
            'device_name': device_name,
            'app_alias': app_alias,
        })['app_name'].strip()

    def clear_datastore(self):
        """This function clears datastore of records."""
        self._logs.drop()
        self._device.drop()
        self._app_name.drop()
        self._start_times.drop()
