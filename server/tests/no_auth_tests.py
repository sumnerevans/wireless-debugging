"""
Tests the no authorization implementation of the user management interface class
Almost everything is hard coded, so we're just checking if those hard-coded
values are returned.

These are pretty trivial tests.
"""

from user_management_interfaces import no_auth
from bottle import request, response

def test_get_login():
    """ Verify that the login UI doesn't exist, and that a blank HTML page is
        returned.
    """
    umi = no_auth.NoAuth()
    base_url = "http://0.0.0.0:80"

    assert umi.get_login_ui(base_url) == ""


def test_user_logged_in():
    """ Verify that the no authorization user management interface doesn't care
        about user logins and always returns true.
    """
    umi = no_auth.NoAuth()
    assert umi.is_user_logged_in(request)


def test_handle_login():
    """ Verify that the no authorization use management interface always lets
        the user through.
    """
    umi = no_auth.NoAuth()
    assert umi.handle_login("", request, response) == (True, "")


def test_get_api_key():
    """ Verify that there are no api-keys being passed around in no
        authorization mode.
    """
    umi = no_auth.NoAuth()
    assert umi.get_api_key_for_user(request) == ""


def test_find_websockets():
    """ The only sort of non-trivial test, verifies that
        find_associated_websockets says to broadcast to all websocket
        connections.
    """
    umi = no_auth.NoAuth()
    api_key = ""
    websockets = []
    for i in range(5):
        websockets.append(request.environ.get("wsgi.websocket"))
        
    assert umi.find_associated_websockets(api_key, websockets) == websockets
