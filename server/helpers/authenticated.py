"""
Defines the Authenticated Decorator which forces the user to be authenticated
to perform the request.
"""

import functools

from bottle import request, redirect
from helpers.config_manager import ConfigManager


def authenticated():
    """ Defines an authenticated decorator, which verifies that the user is
        logged in.

    When a function is associated with this decorator, if the function returns
    a dict this function will append a bool indicating whether or not the user
    is logged in.

    Args:
        None, but calls the user management interface to determine if the
        user is logged in.
    Returns:
       The dictionary the contained function returns, with an additional entry
       named 'logged_in' that maps to a boolean that indicates whether or not
       the user is logged in.

       If the contained function does not return a dict, then this function
       returns whatever the contained function returns.

       This function will also redirect the user to the login page if the user
       is not logged in.
    """

    def decorator(function):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            is_user_logged_in = ConfigManager.user_management_interface.is_user_logged_in(
                request)
            if not is_user_logged_in:
                redirect('/login_page')

            webpage_arguments = function(*args, **kwargs)

            api_key = ConfigManager.user_management_interface.get_api_key_for_user(
                request)
            if isinstance(webpage_arguments, dict):
                webpage_arguments['logged_in'] = is_user_logged_in
                webpage_arguments['api_key'] = api_key

            return webpage_arguments

        return wrapper

    return decorator
