from django import template

register = template.Library()

@register.filter('multiply')
def multiply(x,y):
    print(1, x)
    print(2, y)
    return x * y




