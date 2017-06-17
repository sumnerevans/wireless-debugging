"""
Manages CLI arguments and retrieving arguments from the  configuration YAML.
"""
import argparse
import os

import yaml

from datastore_interfaces import *
from user_management_interfaces import *


class ConfigManager(object):
    _config_manager = None
    user_management_interface = None
    datastore_interface = None

    def __init__(self):
        self._config = {}

        # Read configuration from command line arguments.
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-c',
            '--config',
            type=str,
            default='config.yaml',
            help='the config file to use (defaults to "config.yaml")')
        parser.add_argument(
            '--hostname',
            type=str,
            help='the hostname to expose the application over')
        parser.add_argument(
            '-p',
            '--port',
            type=int,
            default=80,
            help='the port to expose the application on')
        parser.add_argument(
            '-u',
            '--user-management-interface',
            help='the User Management Interface to use')
        parser.add_argument(
            '-d',
            '--datastore-interface',
            help='the Datastore Interface to use')
        parsed_args = parser.parse_args()

        # Read config from file
        if os.path.isfile(parsed_args.config):
            with open(parsed_args.config) as config:
                self._config = yaml.load(config)

        for arg, value in vars(parsed_args).items():
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
