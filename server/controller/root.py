"""
Root Controller
"""
import functools

from bottle import abort, post, redirect, request, response, route, static_file
from kajiki_view import kajiki_view
from markupsafe import Markup

from helpers.config_manager import ConfigManager


def authenticated():
    """ Defines an authenticated decorator, which verifies that the user is logged
        in.

        When a function is associated with this decorator, if the function
        returns a dict this function will append a bool indicating whether or
        not the user is logged in.

        Args:
            None, but calls the user management interface to determine if the
            user is logged in.
        Returns:
            The dictionary the contained function returns, with an additional
            entry named 'logged_in' that maps to a boolean that indicates
            whether or not the user is logged in.

            If the contained function does not return a dict, then this function
            returns whatever the contained function returns.

            This function will also redirect the user to the login page if the
            user is not logged in.
    """

    def decorator(function):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            is_user_logged_in = (ConfigManager.user_management_interface.
                                 is_user_logged_in(request))
            if not is_user_logged_in:
                redirect('/login_page')

            webpage_arguments = function(*args, **kwargs)

            api_key = (ConfigManager.user_management_interface.
                       get_api_key_for_user(request))
            if isinstance(webpage_arguments, dict):
                webpage_arguments['logged_in'] = is_user_logged_in
                webpage_arguments['api_key'] = api_key

            return webpage_arguments

        return wrapper

    return decorator


@route('/')
@kajiki_view('index')
@authenticated()
def index():
    """ The log streaming dashboard, this is where logs go when they're
        streamed.

    Checks if the user is logged in. If not, redirects them to a login page.
    Otherwise sends them to the log viewing dashboard, where the logs are
    streamed to.

    Args:
        None
    Returns:
        If the user is not logged in, redirects them to the login page.
        Otherwise this returns a webpage specified in the kajiki view decorator
        with the additional values in a dictionary.
        page: The page that Kajiki should show.
        api_key: The Web UI user's API key.

    """

    return {
        'page': 'index',
    }


@route('/current')
@kajiki_view('current')
@authenticated()
def current():
    """ Show current streaming logs. """

    return {
        'page': 'current',
    }


@route('/historical')
@kajiki_view('historical')
@authenticated()
def historical():
    """" Retrieve stored data from datastore. """

    return {
        'page': 'historical',
    }


@route('/resources/<filepath:path>')
def static(filepath):
    """
    Routes all of the resources
    http://stackoverflow.com/a/13258941/2319844
    """
    return static_file(filepath, root='resources')


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
    if controller.user_management_interface.is_user_logged_in(request):
        redirect('/')

    return {
        'login_fields':
        Markup(ConfigManager.user_management_interface.get_login_ui()),
        'logged_in':
        ConfigManager.user_management_interface.is_user_logged_in(request),
    }


@post('/login')
def handle_login():
    """ Takes a login form and verifies the user's identity. """
    login_successful, error_message = (
        ConfigManager.user_management_interface.handle_login(
            request.forms, request, response))

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
