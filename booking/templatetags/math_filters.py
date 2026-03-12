from django import template

register = template.Library()

@register.filter
def div(value, divisor):
    try:
        return float(value) / float(divisor)
    except:
        return 0
