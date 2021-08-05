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



# @register.filter
# def get_tipo_fornecedor(obj):
#     return obj.get_model_type


    