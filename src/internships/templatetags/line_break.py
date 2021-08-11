import re

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def line_break(context, value):
    if type(value) == str:
        value = re.sub(r'^\s+|\n|\s+$', '<br>', value)
    return value