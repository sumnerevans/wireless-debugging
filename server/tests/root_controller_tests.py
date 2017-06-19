"""
Tests for the Root Controller
"""
import pytest
import bottle

from controller import root


def test_static_routing():
    # Ensure that you can retrieve the JS and resources. (Wrap this in a
    # pytest.warns so that it allows for ResourceWarnings becuase of opening,
    # but not closing the resource files.)
    with pytest.warns(ResourceWarning):
        root.static('js', 'require.js')
        root.static('resources', 'css/app.css')

    # Ensure that Bottle raises an exception on files not in the js or
    # resources directories.
    with pytest.raises(bottle.HTTPError) as e_info:
        root.static('helpers', 'util.py')
    assert e_info.value.status == '404 Not Found'

    # Assert that when it can't find the file, the status code is 404.
    assert root.static('js', 'not-here.js').status == '404 Not Found'
