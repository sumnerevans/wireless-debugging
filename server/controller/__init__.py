"""
Controller Module
"""

import user_management_interfaces
import controller.root
import controller.sessions
import controller.websocket

# Curse you extrememly long variable name...
user_management_interface = user_management_interfaces.no_auth.NoAuth()
