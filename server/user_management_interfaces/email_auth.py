"""
A simple form of 'authorization' where the user enters their email. 
THIS ISN'T A SECURE METHOD OF AUTHORIZATION. This just enables a server to
direct log files to specific machines, rather than having the logs be broadcast
to all web UI websockets.
"""

import os.path

from user_management_interfaces import user_management_interface_base

class EmailAuth(user_management_interface_base.UserManagementInterfaceBase):
    """ A User Management Interface that uses emails to direct logs to
        the appropriate Web UI.
    """

    def __init__(self):
        self.user_key_table = "key_table.txt"

    def get_login_ui(self, base_url):
        """Unused, but abstract so needs an implementation"""
        return ""

    def is_user_logged_in(self, request):
        """ If a stashed cookie is found indicating that the user has logged in,
            return true. Otherwise return false.

        Args:
            A Bottle request object
        Returns:
            Always returns a boolean true
        """

        # Check if the user's already logged in,
        if request.get_cookie("api_key"):
            # ... and that the api key they have is valid.
            api_key = request.get_cookie("api_key")
            if self.exists_in_table(api_key, False):
                return True
            
        return False

    def handle_login(self, form_data, request, response):
        """Function is unused, but is abstract so needs to be implemented"""
        return (True, "")

    def get_api_key_for_user(self, request):
        """Unused, but abstract so needs implementation"""
        return ""

    def find_associated_websockets(self, api_key, websocket_connections):
        """ We can't tell the difference between users,
            so we just broadcast to everyone

        Args:
            api_key: The API Key, but this is an arbitrary value
            websocket_connections: The list of WebSockets that go to web UIs
        Returns:
            The list of WebSockets that go to web UIs
        """
        return websocket_connections

    def exists_in_table(self, user_key, is_user):
        """ Checks if a given API key or user exists in the user to api key
            table.

        Args:
            user_key: The key to verify in the table. This can either be an API 
                      key or a user email.
            is_user: Boolean, if this is true, then a user email was passed in,
                              if this is false, then an api key was passed in.
        Returns:
            Boolean, true if the key existed in the table, false otherwise.
        """

        # If the table doesn't exist yet, then they can't exist in the table
        if not os.path.isfile(self.user_key_table):
            return False

        user_key_file = open(self.user_key_table, 'r')
        # Splits each row of the file by comma, yielding an email and an api key
        # I'm not sorry ... probably be refactored soon
        user_key_table = [(line.split(',')[0], line.split(',')[1]) 
                          for line in user_key_file.read().splitlines()]

        # 0 is for users, 1 is for api keys
        check_index = 0 if is_user else 1

        if any(user_key == key[check_index] for key in user_key_table):
            return True

        return False
