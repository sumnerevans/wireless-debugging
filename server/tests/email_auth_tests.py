"""
Tests the email authorization implementation of the user management interface.
"""

import os

from user_management_interfaces import email_auth
from bottle import response
from tests.test_classes import DummySocket, DummyForm, DummyRequest


def test_get_login():
    """ Verify that the login UI is read from fie and returned properly.

        This test needs to run from the server folder so that the pathing is
        consistent.
    """
    umi = email_auth.EmailAuth()

    with open('user_management_interfaces/email_login.xhtml', 'r') as fin:
        expected_html = fin.read()

    assert umi.get_login_ui() == expected_html % '/login'


def test_exists_in_table():
    """ Tests that the checking if a user or an API key exists in the table
        works. Also verifies that if they don't exist that this function returns
        false. This is higher up because later functions rely on 
        _exists_in_table().
    """
    umi = email_auth.EmailAuth()
    # This overrides the default table file
    umi.user_key_table = 'temp_file.txt'

    test_username = 'hi@gmail.com'

    assert not umi._exists_in_table(test_username, 'user')
    assert not umi._exists_in_table(test_username, 'api_key')

    with open('temp_file.txt', 'w') as user_table:
        user_table.write('%s,%s\n' % (test_username, test_username))
        
    assert umi._exists_in_table(test_username, 'user')
    assert umi._exists_in_table(test_username, 'api_key')

    os.remove(umi.user_key_table)


def test_user_not_logged_in():
    """ Verify that if the API cookie is not in the user's browswer that the
        login check returns false.
    """
    umi = email_auth.EmailAuth()
    request = DummyRequest()

    assert not umi.is_user_logged_in(request)


def test_user_logged_in():
    """ Verify that if the API cookie is is in the user's browser that the login
        check returns true.
    """
    umi = email_auth.EmailAuth()
    request = DummyRequest()
    request.set_cookie('api_key', 'hello_world')

    assert request.get_cookie('api_key') is not None
    assert not umi.is_user_logged_in(request)


def test_handle_new_login():
    """ Verify that when a new user logs in they'll be added to the user-API key
        table, and verify that they successfully log in.
    """
    umi = email_auth.EmailAuth()
    # It'd be nice to actualy make this a temp file.
    # This overrides the default table file
    umi.user_key_table = 'temp_file.txt' 

    form = DummyForm({
        'username': 'test@test.com',
    })
    request = DummyRequest()
    request.add_form(form)

    result = umi.handle_login(form, request, response)

    assert result == (True, 'New user! Adding to users table.')

    os.remove(umi.user_key_table)


def test_handle_returning_login():
    """ Verify that when a user returns and logs in again, they are accepted
        without any diagnostic messages.
    """
    umi = email_auth.EmailAuth()
    # It'd be nice to actualy make this a temp file.
    # This overrides the default table file
    umi.user_key_table = 'temp_file.txt'

    form = DummyForm({
        'username': 'test@test.com',
    })
    request = DummyRequest()
    request.add_form(form)

    test_username = 'test@test.com'

    with open('temp_file.txt', 'w') as user_table:
        user_table.write('%s,%s\n' % (test_username, test_username))
    
    result = umi.handle_login(form, request, response)

    assert result == (True, '')

    os.remove(umi.user_key_table)

    
def test_get_api_key():
    """ Verify that when the user logs in with an existing username, the 
        corresponding API key is returned.
    """
    umi = email_auth.EmailAuth()
    # It'd be nice to actualy make this a temp file
    # This overrides the default table file
    umi.user_key_table = 'temp_file.txt'

    request = DummyRequest()

    test_username = 'test@test.com'
    test_api_key = 'TestAPIKEY'

    form = DummyForm({
        'username': test_username,
    })
    request.add_form(form)

    with open('temp_file.txt', 'w') as user_table:
        user_table.write('%s,%s\n' % (test_username, test_api_key))

    assert umi.get_api_key_for_user(request) == test_api_key

    os.remove(umi.user_key_table)


def test_find_websockets():
    """ Verify that given an API key and a set of websocket connections, a list
        of websocket connections corresponding to the API key are returned.
    """

    umi = email_auth.EmailAuth()

    websockets = {
        'a': [DummySocket() for i in range(5)],
        'b': [DummySocket() for i in range(3)],
        'c': [DummySocket() for i in range(7)],
    }

    for api_key in ('a', 'b', 'c'):
        assert umi.find_associated_websockets(api_key, 
                                              websockets) == websockets[api_key]
