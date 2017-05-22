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
    """Spits out a specified entry from the config yaml file"""
    if helpers.config_yaml is None or force_reload:
        with open('app.yaml') as config:
            helpers.config_yaml = yaml.load(config)

    if key in helpers.config_yaml:
        return helpers.config_yaml[key]

    return None
