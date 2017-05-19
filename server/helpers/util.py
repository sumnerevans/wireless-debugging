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
