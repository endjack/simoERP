from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='format')
def format(value):
    a = '{:,.2f}'.format(float(value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')

@register.filter(name='has_group') 
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False

@register.filter(name="no_dot")
def replace_dot(value):
    text = str(value)
    return text.replace(".","")

@register.filter(name="replace_input_dot")
def replace__input_dot(value):
    text = str(value)
    return text.replace(",",".")

@register.filter(name="replace")
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)


    