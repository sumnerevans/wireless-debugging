# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Controller Module
"""

import controller.root
import controller.sessions
import controller.websocket

from helpers.util import from_config_yaml

# Replace MongoDataStoreInterface with your desired datastore interface.
from datastore_interfaces import *

# Replace email_auth with your desired user management interface
from user_management_interfaces import *

# This needs to be accessed by root and websockets, so it's being kept one level
# above.
# Also replace email_auth.EmailAuth() with your desired user management
# interface in the config.yaml file.
# Also replace MongoDataStoreInterface() with your desired datastore interface
# in the config.yaml file.
user_management_interface = eval(from_config_yaml('user_management_interface'))
datastore_interface = eval(from_config_yaml('datastore_interface'))
