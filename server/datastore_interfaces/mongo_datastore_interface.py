from pymongo import MongoClient

from datastore_interfaces.base_datastore_interface import DatastoreInterface

class MongoDatastoreInterface(DatastoreInterface):
    def __init__(self, hostname=None):
        self._client = MongoClient()
        self._db = self._client.test_database
        self._logs = self._db.logs
        self._dev = self._db.dev
        self._sessions = self._db.sessions
           
    def add_in_log(self):
        '''
        add in log to logs tables 
        '''

    def add_devices_apps(self):
        '''
        add devices and apps
        '''
        
    def get_devices_apps(self):
        '''
        return devices and apps
        '''

    def add_user(self, webIdToken):
        '''
        add session
        '''
        print (self._sessions)

    def get_user(self, webIdToken):
        '''
        get the current user
        '''
        return 'tikalin'

    def get_users(self):
        '''
        get sessions s
        '''
    
    
