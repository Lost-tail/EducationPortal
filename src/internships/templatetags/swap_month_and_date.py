from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def swap_month_and_date(context, value):
    if type(value) is not str:
        return value
    try:
        d = value.split('/')
        return '/'.join((d[1], d[0], d[2]))
    except IndexError:
        return value