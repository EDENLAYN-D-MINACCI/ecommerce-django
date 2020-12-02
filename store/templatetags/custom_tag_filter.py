from django import template


register = template.Library()

@register.filter(name='formatPrice')
def isPriceDecimal(price):
    if (float(price).is_integer()): return int(price)
    else: return round(price, 2)

@register.filter(name='sum')
def cartTotal(selected_products):
     total = 0
     for product_value in selected_products:
          total += product_value
     return product_value


