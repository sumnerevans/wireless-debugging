"""
Tests the email authorization implementationo of the user management interface.
"""

import os

from user_management_interfaces import email_auth
from bottle import request, response


def test_get_login():
    """ Verify that the login UI is read from fie and returned properly. 
        This test needs to run from the server folder so that the pathing is
        consistent
    """
    umi = email_auth.EmailAuth()
    base_url = 'http://0.0.0.0:80'

    # Ugly format because we can't have any changes in whitespace so that the 
    # test works properly.
    target = '''<form action="/login" method="post" accept-charset="UTF-8" class="form-horizontal">
    <div class="form-group">
        <label class="col-sm-2 control-label">Email:</label>
        <div class="col-sm-10">
            <input class="form-control" type="text" name="username" placeholder="Enter your email here..."/>
        </div>
    </div>
    <div class="form-group">
        <div class="col-sm-10 col-sm-offset-2">
            <button type="submit" class="btn btn-default">Submit</button>
        </div>
    </div>
</form>'''

    assert umi.get_login_ui(base_url) == target


def test_user_not_logged_in():
    """ Verify that if the api cookie is not in the user's browswer that the
        login check returns false.
    """
    umi = email_auth.EmailAuth()
    assert not umi.is_user_logged_in(request)


# This test needs to be fixed since it relies on cookies
def test_user_logged_in():
    """ Verify that if the api cookie is is in the user's browser that the login
        check returns true.
    """
    umi = email_auth.EmailAuth()
    request.set_cookie('api_key', 'hello_world')

    assert request.get_cookie('api_key') is not None
    assert not umi.is_user_logged_in(request)


def test_handle_new_login():
    """ Verify that when a new user logs in they'll be added to the user-api key
        table, and verify that they successfully log in.
    """
    umi = email_auth.EmailAuth()
    # It'd be nice to actualy make this a temp file
    umi.user_key_table = "temp_file.txt" 

    

    os.remove(umi.user_key_table)

