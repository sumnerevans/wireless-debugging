"""
Utility Functions
"""
import json
from datetime import datetime
import yaml
from markupsafe import Markup
import helpers


def serialize_to_json(data):
    """ Serialize an object to JSON, ensuring that the datetimes are formatted
    according to RFC 3339

    Args:
        obj: the object to serialize to JSON
    """

    # Define the actual datetime serializer
    # See: https://stackoverflow.com/questions/8556398/generate-rfc-3339-timestamp-in-python#8556555
    def datetime_serializer(element):
        if isinstance(element, datetime):
            return element.isoformat("T") + "Z"

    return json.dumps(data, default=datetime_serializer)


def from_config_yaml(key, force_reload=False):
    """Spits out a specified entry from the config yaml file

    This function takes the key value in the config value and gives
    the corresponding value from config.yaml file which, if none is given,
    is the app.yaml file.

    Args:
        key: Key value in the config file that will return the value
        force_reload (:obj:`bool`, optional): Whether or not to force the
            configs to be reloaded from disk. Defaults to False.
    """
    if helpers._config_yaml is None or force_reload:
        with open('config.yaml') as config:
            helpers._config_yaml = yaml.load(config)

    if key in helpers._config_yaml:
        return helpers._config_yaml[key]

    return None
