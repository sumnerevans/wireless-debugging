"""
Tests for the Utility functions in helpers.util
"""
from datetime import datetime

from helpers import util

def test_json_serialize():
    """ Test that the JSON Serialization works as expected. """
    time = datetime.strptime('2017-06-15 17:41:45', '%Y-%m-%d %H:%M:%S')
    object_to_serialize = {
        'time': time,
        'app': 'Wireless Debug',
        'isAwesome': True,
        'coolThings': ['Travis CI', 'Codecov'],
        'pi': 3.14,
        'nested': {
            'now': time,
            'inAnArray': [time, time],
        }
    }

    expected_result = ' '.join([
        '{"coolThings": ["Travis CI", "Codecov"], "app": "Wireless Debug",',
        '"isAwesome": true, "nested": {"inAnArray": ["2017-06-15T17:41:45Z",',
        '"2017-06-15T17:41:45Z"], "now": "2017-06-15T17:41:45Z"},',
        '"time": "2017-06-15T17:41:45Z", "pi": 3.14}'
    ])

    assert util.serialize_to_json(object_to_serialize) == expected_result

def test_from_config_yaml():
    """ Tests that retrieving data from the config file works as expected. """
    assert util.from_config_yaml('hostname') == '0.0.0.0'
    assert util.from_config_yaml('nothing') is None
