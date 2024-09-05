from django import template
from django.utils.http import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.filter(name='getattr')
def getattrfilter(o, attr):
    attrs = attr.split('.')
    try:
        data = o
        for a in attrs:
            data = getattr(data, a)
        return data
    except:
        return ''