from django import template

register = template.Library()


@register.filter
def src_from_keys(value):
    return value.replace("(", "").replace(")", "").replace("'", "").split(",")[0]


@register.filter
def dst_from_keys(value):
    return value.replace("(", "").replace(")", "").replace("'", "").split(",")[1]


@register.filter
def value_from_key(dictionary, key):
    return dictionary.get(key)