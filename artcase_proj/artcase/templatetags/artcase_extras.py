from django import template

register = template.Library()

@register.simple_tag
def get_verbose_name(model, case=False):
    name = model._meta.verbose_name
    if case == 'title':
        name = name.title()
    return name

@register.simple_tag
def get_verbose_name_plural(model, case=False):
    name = model._meta.verbose_name_plural
    if case == 'title':
        name = name.title()
    return name

@register.simple_tag
def get_create_url(model):
    return model.get_create_url()

@register.simple_tag
def get_list_url(model):
    return model.get_list_url()

@register.simple_tag
def get_update_url(model, pk):
    return model.get_update_url(pk)

@register.simple_tag
def get_delete_url(model, pk):
    return model.get_delete_url(pk)
