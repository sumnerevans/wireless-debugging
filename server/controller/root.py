"""
Root Controller
"""
import functools
import io
import sys

from bottle import abort, post, redirect, request, response, route, static_file, get
from kajiki_view import kajiki_view
from markupsafe import Markup

import parsing_lib
from helpers.config_manager import ConfigManager as config

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
            is_user_logged_in = config.user_management_interface.is_user_logged_in(
                request)
            if not is_user_logged_in:
                redirect('/login_page')

            webpage_arguments = function(*args, **kwargs)

            api_key = config.user_management_interface.get_api_key_for_user(
                request)
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


@get('/upload_logs')
@kajiki_view('upload_logs')
@authenticated()
def upload_logs():
    """ This is to get the webpage. """
    return {
        'page': 'upload_logs',
        'raw_logs': '',
    }


@post('/upload_logs')
@kajiki_view('upload_logs')
@authenticated()
def upload_logs():
    """ This is where the logs will be uploaded from the page. """
    os_type = request.forms.get('os_type')
    log_file = request.files.get('log_file')
    raw_text = request.forms.get('message')
    return_val = {
        'page': 'upload_logs',
        'raw_logs': raw_text,
        'log_entries': Markup(''),
    }

    if log_file:
        message = str(log_file.file.read(), 'utf-8')
    elif raw_text.strip():
        message = raw_text
    else:
        return_val['flash'] = {
            'content': 'Please upload a file or paste logs.',
            'cls': 'error',
        }
        return return_val

    try:
        parsed_message = parsing_lib.LogParser.parse(message, os_type)
        log_entries = parsing_lib.LogParser.convert_to_html(parsed_message)
        return_val['log_entries'] = Markup(log_entries)
    except Exception as e:
        return_val['flash'] = {
            'content': 'Log format error: %s' % str(e),
            'cls': 'error',
        }
    finally:
        return return_val


@route('/<resource_root>/<filepath:path>')
def static(resource_root, filepath):
    """
    Routes all of the resources
    http://stackoverflow.com/a/13258941/2319844
    """
    if resource_root not in ('resources', 'js'):
        abort(404)

    return static_file(filepath, root=resource_root)


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
