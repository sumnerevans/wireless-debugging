#! /usr/bin/env python3

"""
Defines the Kajiki View Decorator
"""

import functools

from helpers import util
from kajiki import FileLoader, XMLTemplate

loader = FileLoader('template')
loader.extension_map['xhtml'] = XMLTemplate


def kajiki_view(template_name):
    """
    Defines the kajiki_view decorator

    Used code example from here:
    https://buxty.com/b/2013/12/jinja2-templates-and-bottle/ but customized for
    kajiki instead
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)

            if isinstance(response, dict):
                # If the decorated function returns a dictionary, throw that to
                # the template
                Template = loader.load('%s.xhtml' % template_name)

                t = Template({
                    **response,
                    **util.extra_template_context()
                })
                return t.render()
            else:
                return response

        return wrapper

    return decorator
