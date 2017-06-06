"""
Tests the email authorization implementationo of the user management interface.
"""

from user_management_interfaces import email_auth
from bottle import request, response


def test_get_login():
    """ Verify that the login UI is read from fie and returned properly. 
        This test needs to run from the server folder so that the pathing is
        consistent
    """
    umi = email_auth.EmailAuth()
    base_url = 'http://0.0.0.0:80'

    # Ugly format because we can't have any changes in whitespace
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

