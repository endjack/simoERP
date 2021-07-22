from django import template

register = template.Library()

@register.filter(name='format')
def format(value):
    a = '{:,.2f}'.format(float(value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()



# @register.filter
# def get_tipo_fornecedor(obj):
#     return obj.get_model_type


    