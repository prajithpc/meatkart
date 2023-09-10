from django import template

register = template.Library()


@register.simple_tag()


# def call_price(product_price_per_kg,product_discount):
#     if product_discount is None or product_discount is 0:
#         return product_price_per_kg
#     else:
        
        
#         sellprice = product_price_per_kg
#         sellprice = product_price_per_kg - (product_price_per_kg * product_discount/100)
#         return sellprice

def call_price(product_price_per_kg, product_discount):
    try:
        product_price_per_kg = float(product_price_per_kg)
        product_discount = float(product_discount)
    except ValueError:
        return product_price_per_kg
    
    if product_discount is None or product_discount == 0:
        return product_price_per_kg
    
    sellprice = product_price_per_kg - (product_price_per_kg * product_discount / 100)
    return sellprice
