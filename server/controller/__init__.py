"""
Controller Module
"""

import user_management_interfaces
import controller.root
import controller.sessions
import controller.websocket
from datastore_interfaces.mongo_datastore_interface import MongoDatastoreInterface

# Curse you extrememly long variable name...
user_management_interface = user_management_interfaces.no_auth.NoAuth()
_current_guid = None
_datastore_interface = MongoDatastoreInterface()
