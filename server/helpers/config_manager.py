"""
Manages CLI arguments and retrieving arguments from the  configuration YAML.
"""
import argparse
import yaml

from datastore_interfaces import *
from user_management_interfaces import *


class ConfigManager(object):
    _config_manager = None
    user_management_interface = None
    datastore_interface = None

    def __init__(self):
        # Read config from file
        with open('config.yaml') as config:
            self._config = yaml.load(config)

        # Read configuration from command line arguments.
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--hostname',
            type=str,
            help='the hostname to expose the application over')
        parser.add_argument(
            '-p',
            '--port',
            type=str,
            help='the port to expose the application on')
        parser.add_argument(
            '-u',
            '--user-management-interface',
            help='the User Management Interface to use')
        parser.add_argument(
            '-d',
            '--datastore-interface',
            help='the Datastore Interface to use')

        command_line_args = vars(parser.parse_args())
        for arg, value in command_line_args.items():
            if value is not None or arg not in self._config:
                self._config[arg] = value

        ConfigManager.datastore_interface = eval(
            self._config.get('datastore_interface', None))
        ConfigManager.user_management_interface = eval(
            self._config.get('user_management_interface', None))

    @staticmethod
    def reset():
        ConfigManager._config_manager = ConfigManager()

    @staticmethod
    def get(config_name, default=None):
        if ConfigManager._config_manager is None:
            ConfigManager._config_manager = ConfigManager()

        return ConfigManager._config_manager._config.get(config_name, default)
