from pymongo import MongoClient

import datastore_interfaces

class DatastoreInterface(object):
    """ Sets up the datastore interface. """
    """TO DO: Pydoc and API Spec """
    
    def __int__(self, **kwargs):
        """ Set up datastore interface 

        Args:
            

        """
           
    def store_logs(self, api_key, device_name, app_name, start_time, os_type, log_entries):
        '''Add in log to logs tables

        Store a set of log entries to the datastore. This function may be called multiple times per session, so it must append the log entries in the storage mechanism.

        Args
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started
            os_type: the OS type (iOS or Android)
            log_entries: the log entries to store
        '''

    def set_session_over(self, api_key, device_name, app_name, start_time):
        """Set session is over

        Called to indicate to the datastore that the session is over. This can set a flag on the session in the datastore indicating that it should not be modified, for example.

        Args:
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started

        """
    def retrieve_logs(self, api_key, device_name, app_name, start_time):
        """Retrieve logs for given section

        Retrieve the logs for a given session.

        Args:
            api_key: the API Key to retrieve logs for
            device_name: the name of the device to retrieve logs for
            app_name: the name of the app to retrieve logs for
            start_time: the time that the session started

        Returns:
        

        """
    def retrieve_devices_and_apps(self, api_key):
        """retrieves devices and apps

        """

    def retrieve_sessions(self, api_key, device, app):
        """
        sessions 
        """

    def add_device_app(self, device, app):
        '''
        add devices and apps
        '''

    def get_user(self, webIdToken):
        '''
        get the current user
        '''

    
    
    
