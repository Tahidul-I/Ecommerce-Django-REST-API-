from django import template
register = template.Library()
@register.filter
def multiply(quantity, price):
    try:
        return int(quantity) * float(price)
    except (ValueError, TypeError):
        return None
    
@register.filter
def subtract(sub_total,discount):
    savings = float(sub_total)*float(discount)/100
    return float(sub_total) - savings

@register.filter
def discount(sub_total,discount_percentage):
    
    return float(sub_total)*float(discount_percentage)/100