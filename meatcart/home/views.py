from collections import UserDict
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from django.core.exceptions import ObjectDoesNotExist
from carts.models import *
from.templatetags.product_tags import call_price

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import AddressForm

from orders.models import*
from django.contrib import messages
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


# def checkout(request):
#     return render(request,'home/checkout.html')


def order_list(request):
    return render(request,'admin')


def checkout(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')  # Redirect to the address page after saving

    else:
        form = AddressForm()

    total = 0
    quantity = 0
    tax = 0
    grand_total = 0
    cart_items = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cartitem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            product_price_per_kg = float(cart_item.product.product_price_per_kg)
            product_discount = float(cart_item.product.product_discount)
            product_total = call_price(product_price_per_kg, product_discount) * cart_item.quantity
            total += product_total
            quantity += cart_item.quantity


            cart_item.product_total = product_total 


            if cart_item.quantity > cart_item.product.product_available_stock:
                messages.warning(request,"no available stock")
                return redirect('cart')



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

    order = Order.objects.filter(user=request.user).latest('created_at')
    
    context = {
        'order': order
    }

    return render(request,'home/success.html', context)


def wishlist(request):
    
    wish_items = Wishitem.objects.filter(user=request.user)
    context = {
        'wish_items':wish_items
    }
    return render(request,'home/wishlist.html',context)

def addtowishlist(request):
    if request.method=="POST":
        product_id = request.POST.get('product.id')
        product_var= Product.objects.get(id=int(product_id))


        wish_item, created = Wishitem.objects.get_or_create(user=request.user, product=product_var)

        if not created:
            wish_item.quantity += 1
            wish_item.save()

        return HttpResponseRedirect(reverse('wishlist'))
    
    product_id = request.GET.get('product_id')
    if product_id:
        product_var = Product.objects.get(id=int(product_id))

        # Instead of handling DoesNotExist and create, use get_or_create
        wish_item, created = Wishitem.objects.get_or_create(user=request.user, product=product_var)

        if not created:
            wish_item.quantity += 1
            wish_item.save()

        return HttpResponseRedirect(reverse('wishlist'))
    
    return HttpResponseRedirect(reverse('products_home'))


def deletefromwishlist(request, product_id):
    # Retrieve the wish item from the wishlist by the product ID and the current user
    wish_item = get_object_or_404(Wishitem, user=request.user, product_id=product_id)
    # Delete the wish item from the database
    wish_item.delete()
    # Redirect the user back to the wishlist page
    return redirect('wishlist')


@login_required
def profile(request):
    print("sree")
    user = request.user
    orders=Order.objects.filter(payment__user = user, is_ordered=True).order_by('created_at')
    orders_count=orders.count()
    
    context={
        'orders_count': orders_count,
        'orders': orders,
    }
    return render(request,'home/profile.html',context)

def details(request):
    return render(request,'home/order_detail.html')

@login_required
def address(request):
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'home/address.html', {'addresses': addresses})


# def my_orders(request):
#     orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    
#     context={
#         'orders':orders,
#     }
#     return render(request,'home/my_orders.html',context)


def my_orders(request):
    print("hellooo")
    user = request.user
    orders = Order.objects.filter(payment__user=user, is_ordered=True).order_by('created_at')
    orders_count = orders.count()
    
    context = {
        'orders_count': orders_count,
        'user': user,
        'orders': orders,  # Add the orders queryset to the context
    }
    return render(request, 'home/my_orders.html', context)




@login_required

def address(request):
    return render(request,'home/address.html')