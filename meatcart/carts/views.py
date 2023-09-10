from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404

from home.models import Product
from .models import *

from django.http import HttpResponse

from django.core.exceptions import ObjectDoesNotExist

from home.templatetags.product_tags import call_price

from django.db import transaction
# Create your views here.




def add_cart(request, id):
    product = Product.objects.get(id=id)  # This will get the product

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    with transaction.atomic():
        try:
            cart_item = Cartitem.objects.select_for_update().get(product=product, cart=cart)
            # If the quantity in the cart is already equal to the available stock, do not increment further.
            if cart_item.quantity < product.product_available_stock:
                cart_item.quantity += 1
                cart_item.save()
        except Cartitem.DoesNotExist:
            # If the item is not in the cart, add it with quantity 1, but don't add more than the available stock.
            quantity_to_add = min(1, product.product_available_stock)
            cart_item = Cartitem.objects.create(
                product=product,
                quantity=quantity_to_add,
                cart=cart
            )

    return redirect('cart')


def remove_cart(request,id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=id)
    cart_item = Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,id):
    cart=Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id=id)
    cart_item = Cartitem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0,quantity=0,cart_items=None):
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            product_price_per_kg = float(cart_item.product.product_price_per_kg)
            product_discount = float(cart_item.product.product_discount)
            product_total = call_price(product_price_per_kg, product_discount) * cart_item.quantity
            total += product_total
            quantity += cart_item.quantity


            cart_item.product_total = product_total 


            
        tax = (2*total)/100
        grand_total = total + tax

        # Update the session values with the latest calculated totals
        request.session['total'] = total
        request.session['quantity'] = quantity
        request.session['tax'] = tax
        request.session['grand_total'] = grand_total

    except ObjectDoesNotExist:
        cart_items = None
    try:
        context ={
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax'   : tax,
            'grand_total' : grand_total,
        }
        return render(request,'home/cart.html',context)

    except:
        pass     
            
    return render(request,'home/cart.html')




def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create
    return cart