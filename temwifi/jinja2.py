from jinja2 import Environment
from jinja2.ext import Extension
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env


@register.filter_function
def attr(obj, arg1):
    att, value = arg1.split("=")
    obj.field.widget.attrs[att] = value
    return obj


class DjangoCustomExtraFiltersExtension(Extension):
    def __init__(self, environment):
        super(DjangoCustomExtraFiltersExtension, self).__init__(environment)

        # Filters
        environment.filters["attr"] = attr
