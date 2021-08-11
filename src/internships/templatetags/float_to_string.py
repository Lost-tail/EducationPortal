from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def float_to_string(context, value):
    return f'{value:g}'