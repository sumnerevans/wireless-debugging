#! /usr/bin/env python3

"""
Utility Functions
"""

from datetime import date

import yaml
from markupsafe import Markup

import helpers


def extra_template_context():
    context = {
    }
    return context


def glyphicon(icon_name, *args, **kwargs):
    return Markup('<i class="glyphicon glyphicon-%s %s" %s></i>' % (
        icon_name,
        ' '.join(args),
        ' '.join('%s="%s"' % (k, v) for k, v in kwargs.items())
    ))


def faicon(icon_name, *args, **kwargs):
    return Markup('<i class="fa fa-%s %s" %s></i>' % (
        icon_name,
        ' '.join(args),
        ' '.join('%s="%s"' % (k, v) for k, v in kwargs.items())
    ))

def from_config_yaml(key, force_reload=False):
    """Spits out a specified entry from the config yaml file
    
    This function takes the key value in the config value and gives 
    the corresponding value from config.yaml file which, if none is given,
    is the app.yaml file. 

    Args:
    	key: Key value in the config file that will return the value
	force_reload (:obj:`bool`, optional): Wheter or not to force the configs to be reloaded from disk. Defaults to False.
    
    """
    if helpers._config_yaml is None or force_reload:
        with open('config.yaml') as config:
            helpers._config_yaml = yaml.load(config)

    if key in helpers._config_yaml:
        return helpers._config_yaml[key]

    return None
