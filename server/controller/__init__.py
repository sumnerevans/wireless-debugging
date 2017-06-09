# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Controller Module
"""

import user_management_interfaces
import controller.root
import controller.sessions
import controller.websocket

# Replace no_auth with your desired user management interface
from user_management_interfaces import no_auth

# This needs to be accessed by root and websockets, so it's being kept one level
# above.
# Also replace no_auth.NoAuth() with your desired user management interface.
user_management_interface = no_auth.NoAuth()
