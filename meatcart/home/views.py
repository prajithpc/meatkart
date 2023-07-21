from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from django.core.exceptions import ObjectDoesNotExist
from carts.models import *




# Create your views here.


def index(request):
    banners = Banner.objects.all()
    context = {'banners': banners}
    return render(request, 'home/home.html', context)
    

def products_home(request):
    
    products= Product.objects.all()
    
    context = {
        'products':products,
    }
    return render(request, 'home/shop.html',context)


# def single_product(request,product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'home/product-single.html', {'product':product})
def single_product(request,id):
    product=Product.objects.filter(id = id).first()

    context={
        'product':product,
    }
    return render(request, 'home/product-single.html',context)


def checkout(request):
    return render(request,'home/checkout.html')


def order_list(request):
    return render(request,'admin')


def checkout(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price_per_kg * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        cart_items = None

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'home/checkout.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create
    return cart


def success(request):
    return render(request,'home/success.html')