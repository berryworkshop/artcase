from django.template import Library

register = Library()

@register.filter
def get_class_name(value):
    return value.__class__.__name__