"""
ConfigManager tests
"""
from unittest.mock import patch
import pytest
from helpers.config_manager import ConfigManager


@pytest.yield_fixture(autouse=True)
def reset_config():
    with patch('sys.argv', ['./widb_server.py']):
        yield
        ConfigManager.reset()


def test_get_config():
    """ Tests that retrieving data from the config file works as expected. """
    assert ConfigManager.get('hostname') == '0.0.0.0'
    assert ConfigManager.get('nothing') is None


def test_get_config_with_default():
    assert ConfigManager.get('hostname', 1) == '0.0.0.0'
    assert ConfigManager.get('nothing', 1) == 1


def test_get_config_from_command_line_arg():
    with patch('sys.argv', ['./widb_server.py', '--hostname', '1.1.1.1']):
        ConfigManager.reset()
        assert ConfigManager.get('hostname') == '1.1.1.1'
        assert ConfigManager.get('hostname', '2.2.2.2') == '1.1.1.1'
        assert ConfigManager.get('nothing', 1) == 1
