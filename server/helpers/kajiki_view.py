"""
Defines the Kajiki View Decorator
"""

import functools

from kajiki import FileLoader, XMLTemplate

loader = FileLoader('template')
loader.extension_map['xhtml'] = XMLTemplate


def kajiki_view(template_name):
    """ Defines a kajiki_view decorator

    When a function is annotated with this decorator, if the function returns a
    dict, those values will be passed into the specified template and the
    rendered template will become the output of the function.

    Notes: Used code example from here:
    https://buxty.com/b/2013/12/jinja2-templates-and-bottle/ but customized for
    Kajiki instead

    Args:
        template_name: the name of the xhtml file to use as the template

    Returns:
        decorator: the decorated function
    """

    def decorator(view_func):

        @functools.wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)

            if isinstance(response, dict):
                # If the decorated function returns a dictionary, throw that to
                # the template
                Template = loader.load('%s.xhtml' % template_name)

                t = Template(response)
                return t.render()
            else:
                return response

        return wrapper

    return decorator
