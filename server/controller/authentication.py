"""
Authentication Controller
"""

from bottle import abort, post, redirect, request, response, route, get
from markupsafe import Markup

from helpers.config_manager import ConfigManager as config
from helpers.kajiki_view import kajiki_view


@route('/login_page')
@kajiki_view('login')
def login():
    """ Retrieves the login page from the user management interface and serves
        it to the user.

    Args:
        None
    Returns:
        An HTML webpage containing a UI for the user to log into the website.
        This function returns a webpage specified by the kajiki view decorator.
        This function also returns a subcomponent of a webpage that defines the
        format of the login page, which is specified in the user management
        interface.
    """
    # Redirect to the home page if the user in already logged in.
    if config.user_management_interface.is_user_logged_in(request):
        redirect('/')

    return {
        'page': 'login',
        'login_fields': Markup(config.user_management_interface.get_login_ui()),
        'logged_in':
        config.user_management_interface.is_user_logged_in(request),
    }


@post('/login')
def handle_login():
    """ Takes a login form and verifies the user's identity. """
    login_successful, error_message = (
        config.user_management_interface.handle_login(request.forms, request,
                                                      response))

    # If handle_login returned a string, it means it failed and returned an
    # error message.
    if not login_successful:
        # TODO: Make better error handling
        print('Something went wrong!:', error_message)
        abort(403, "Login failed, error: %s" % error_message)
    else:
        redirect('/')


@route('/logout')
def logout():
    """ Logs the user out of the web UI interface.

    Functionally this just takes the API key cookie on the user's machine and
    sets it to a dummy value and expires it immediately.

    Uses the bottle response object, which can modify cookies on a user's
    browser.

    Returns a modified, expried cookie on the user's browser.
    Also redirects to this website's index page, which should redirect to
    the login page.
    """

    response.set_cookie('api_key', '', expires=0)
    redirect('/')
