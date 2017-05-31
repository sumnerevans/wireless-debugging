from pymongo import MongoClient

import datastore_interfaces

class DatastoreInterface(object):
    """ Sets up the datastore interface. """
    
    def __int__(self, **kwargs):
        """ Set up datastore interface 

        Args:
            

        """
           
    def store_logs(self, api_key, device_name, app_name, start_time, os_type log_entries):
        '''add in log to logs tables

        store a set of log entries to the datastore. This function may be called multiple times per session, so it must append the log entries in the storage mechanism.

        Args
            api_key: the API Key associated with the logs
            device_name: the name of the device associated with the logs
            app_name: the name of the app associated with the logs
            start_time: the time that the session started
            os_type: the OS type (iOS or Android)
            log_entries: the log entries to store
        '''

    def add_device_app():
        '''
        add devices and apps
        '''
        
    def get_devices_apps():
        '''
        return devices and apps
        '''

    def add_user(webIdToken):
        '''
        add session
        '''

    def get_user(webIdToken):
        '''
        get the current user
        '''

    def get_users():
        '''
        get sessions s
        '''
    
    
