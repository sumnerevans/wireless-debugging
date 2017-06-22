"""
Root Controller
"""
from bottle import abort, post, redirect, request, response, route, static_file, get
from markupsafe import Markup

import parsing_lib
from helpers.config_manager import ConfigManager as config
from helpers.kajiki_view import kajiki_view
from helpers.authenticated import authenticated


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
def process_uploaded_logs():
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
