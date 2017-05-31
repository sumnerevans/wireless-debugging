# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Root Controller
"""

from bottle import abort, post, redirect, request, response, route, static_file
from helpers.util import from_config_yaml
from kajiki_view import kajiki_view
import controller

@route('/')
@kajiki_view('index')
def index():
    """The log streaming dashboard, this is where logs go when they're streamed
    
    Checks if the user is logged in. If not, redirects them to a login page.
    Otherwise sends them to the log viewing dashboard, 
    where the logs are streamed to

    Args:
        None
    Returns:
        If the user is not logged in, redirects them to the login page
        Returns an HTML webpage to the user if the user is logged in

    """

    # TODO: Decorator?
    if not controller.user_management_interface.is_user_logged_in(request):
        redirect('/login_page')

    # TODO: Probably a proper way to give the API key back, like AJAX
    api_key = controller.user_management_interface.get_api_key_for_user(request)

    return {'page': 'index', 
            'api_key': api_key}


@route('/resources/<filepath:path>')
def static(filepath):
    """
    Routes all of the resources
    http://stackoverflow.com/a/13258941/2319844
    """
    return static_file(filepath, root='resources')

@route('/login_page')
def login():
    """Retrieves the login page from the user management interface
       and serves it to the user

    Args:
        None
    Returns:
        An HTML webpage containing a UI for the user to log into the website
    """
    hostname = from_config_yaml("hostname")
    port = from_config_yaml("port")
    url = "http://" + hostname + ":" + str(port)
    print(request)
    return controller.user_management_interface.get_login_ui(url)

@post('/login')
def handle_login():
    """Takes a login form and verifies the user's identity
    """
    login_successful, err_msg = ( # Parenthesis is grooooss
        controller.user_management_interface.handle_login(request.forms,
                                                          request, response))

    # If handle_login returned a string, 
    # it means it failed and returned an error message
    if not login_successful:
        # TODO: Make better error handling
        print("Something went wrong!:", err_msg)
        abort(404, "Login failed, error: %s" % err_msg)
    else:
        redirect('/')
