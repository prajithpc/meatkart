from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from carts.models import Cartitem,Cart
from .forms import OrderForm
from home.templatetags.product_tags import call_price
import datetime
from home.models import *
import uuid           

from django.shortcuts import render, redirect
from .models import Order, OrderProduct, Payment
from django.contrib.auth.decorators import login_required

from carts.views import _cart_id 

from django.contrib import messages

from admins.views import *

from home.views import *

def generate_order_number():
    # Generate a unique order number using UUID
    return str(uuid.uuid4().int)[:10]  # You can customize the length of the order number as needed


@login_required
def place_order(request):
    print("jijili")
    
    if request.method == 'POST':
        # Get data from the form
        user = request.POST.get('user')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line_1')
        district = request.POST.get('district','')
        city = request.POST.get('city','')
        order_note = request.POST.get('order_note', '')  # Optional field, so provide default value
        payment_type = request.POST.get('payment')
        order_number = generate_order_number()


        # Retrieve cart details from the session or wherever you have stored them
        # For example, you might store cart details in the session like this:
        cart = request.session.get('cart', {})
        total = request.session.get('total', 0)
        tax = request.session.get('tax', 0)
        grand_total = request.session.get('grand_total', 0)


        # Create Payment instance
        payment = Payment.objects.create(
            user=request.user,  # Assuming you have an authenticated user
            payment_id='',  # Add the payment_id if you have one
            payment_method=payment_type,  # Add the payment_method used
            amount_paid=grand_total,
            status='Pending',  # You can set this to 'Pending' for now, and update it later when payment is completed
            order_number=order_number,
        )

        # Create Order instance
        order = Order.objects.create(
            user = request.user,
            payment=payment,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            address_line_1=address_line_1,
            district=district,
            city=city,
            order_note=order_note,
            order_total=grand_total,
            tax=tax,
            status='New',  # Set the initial status to 'New'
            ip=request.META.get('REMOTE_ADDR', ''),  # Get the user's IP address
            is_ordered=False,  # Set is_ordered to False initially
            order_number=order_number,
            
        )


        request.session['address_context'] = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'address_line_1': address_line_1,
            'district': district,
            'city': city,
        }
        


    cart_id = _cart_id(request)
    print("Cart ID:", cart_id)
    cart_items = Cartitem.objects.filter(cart__cart_id=cart_id)   

        # Create OrderProduct instances
    for cart_item in cart_items:
                # Retrieve the Product instance based on the product_id
        product = cart_item.product

                # Calculate the product price (you might have this information stored in your Product model)
        product_price = call_price(product.product_price_per_kg, product.product_discount) * cart_item.quantity

                # Create the OrderProduct instance
        order_product = OrderProduct.objects.create(
            cart_item=cart_item,
            order=order,
            payment=payment,
            user=request.user,  # Assuming you have an authenticated user
            product_price=product_price,
            ordered=False,  # Set ordered to False initially
            order_number=order_number,  
        )
        cart_item.ordered = True
        cart_item.save() 

        request.session['cart'] = {}
        request.session['total'] = total
        request.session['tax'] = tax
        request.session['grand_total'] = grand_total

            # Redirect to a success page or do whatever you want after placing the order
        return redirect('success')  # Replace 'success_page' with the name of your success page URL pattern
        
   

    # If the request method is not POST, just render the checkout page
    return render(request, 'checkout.html')



def orderlist(request):
    orders = Order.objects.all()
    order_data = {}
    for order in orders:
        order_items = order.order_items.all()
        order_data[order] = order_items
    return render(request,'admin/order_list.html', {'order_data': order_data})




def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        new_status = request.POST.get('status')  # Replace with your actual form field name
        if new_status is not None:
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully.')
            return redirect('orderlist')
            # Perform any additional actions or return a response

    return render(request, 'admin/order_list.html', {'order_data': order_data })









def order_detail(request, order_id):
    order = get_object_or_404(Order, order_number=order_id)
    return render(request, 'home/user_order.html', {'order': order})


@login_required

def saved_addresses(request):
    address_context = request.session.get('address_context', None)

    # Clear the session data to avoid reusing it on subsequent requests
    request.session.pop('address_context', None)

    if address_context is None:
        return HttpResponse("No saved address data found.")

    return render(request, 'home/saved_adresses.html', context=address_context)