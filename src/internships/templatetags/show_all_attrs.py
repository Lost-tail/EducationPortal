from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def show_all_attrs(context, value):
    res = []
    for k in dir(value):
        print(k)
        res.append('%r %r\n' % (k, getattr(value, k)))
    return '\n'.join(res)