# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Root Controller
"""

from bottle import route, static_file
from kajiki_view import kajiki_view


@route('/')
@kajiki_view('index')
def index():
    return {'page': 'index'}


@route('/resources/<filepath:path>')
def static(filepath):
    """
    Routes all of the resources
    http://stackoverflow.com/a/13258941/2319844
    """
    return static_file(filepath, root='resources')
