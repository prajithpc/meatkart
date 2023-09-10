
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import *
from django.shortcuts import get_object_or_404,HttpResponse
from home.models import Product, Categories
from django.conf import settings
import os
from home.models import Banner
from django.contrib.auth.decorators import login_required


# from .models import Student
# Create your views here.

def adminlogin(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        pass1=request.POST.get("pass1")
        myuser=authenticate(username=uname,password=pass1)
        if myuser is not None:
            if myuser.is_superuser:
                login(request,myuser)
                messages.success(request,"Login success")
                return redirect('adminhome')
                
            elif myuser is not myuser.is_superuser:
                messages.error(request,"you are not admin")
                return redirect('adminlogin')
                
            
        else:
            messages.error(request, "Invalid Credentials")
            
    # if not request.user.is_authenticated:    
    #     return render(request,'home.html')
    # else:    
    return render(request,'admin/admin_login.html')


def adminhome(request):
    return render(request,'admin/admin_home.html')



def user_list(request):
    data=User.objects.all()
    print(data)
    context={"data":data}
    return render(request,"admin/user_table.html",context)

def user_block(request,id):
    print("hykyu")
    d = User.objects.get(id=id)
    d.is_active = False
    d.save()
    messages.error(request,"Blocked Successfully")
    return redirect("user_list")

def user_unblock(request,id):
    
    d = User.objects.get(id=id)
    d.is_active = True
    d.save()
    messages.success(request,"Unblocked Successfully")
    return redirect("user_list")






# PRODUCTS

def product_list(request):
    products = Product.objects.all()
    categories=Categories.objects.all()
    context = {'products':products, 'categories':categories}
    return render(request, 'admin/product_list.html',context)


def product_add(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('product_category')
        product_image = request.FILES.get('product_image')
        product_description = request.POST.get('product_description')
        product_price_per_kg = request.POST.get('product_price_per_kg')
        product_available_stock = request.POST.get('product_available_stock')
        product_discount = request.POST.get('product_discount')


        try:
            product_discount = int(product_discount)
        except ValueError:
            # Handle the case when the discount is not a valid integer
            product_discount = 0


        product_category=get_object_or_404(Categories, id=category_id)
        products = Product(
            product_name = product_name,
            product_category = product_category,
            product_image = product_image,
            product_description = product_description,
            product_price_per_kg = product_price_per_kg,
            product_discount = product_discount,
            product_available_stock = product_available_stock
        )
        products.save()
        return redirect('product_list')
    
def product_edit(request):
    products = Product.objects.all()
    context = {'products':products}
    return redirect('product_list',context)


def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product_name = request.POST.get('product_name') 
        category_id = request.POST.get('product_category')
        product_image = request.FILES.get('product_image')
        product_description = request.POST.get('product_description')
        product_price_per_kg = request.POST.get('product_price_per_kg')
        product_discount = request.POST.get('product_discount')
        product_available_stock = request.POST.get('product_available_stock')


        try:
            product_discount = int(product_discount)
        except ValueError:
            # Handle the case when the discount is not a valid integer
            product_discount = 0
        
        # Retrieve the updated 'product_thumbnail' field value
        
        # Update other product details
        product.product_name = product_name
        product.product_category = get_object_or_404(Categories, id=category_id)
        # product.product_image = product_image
        product.product_description = product_description
        product.product_price_per_kg = product_price_per_kg
        product.product_discount = product_discount
        product.product_available_stock = product_available_stock   


        if product_image:
            # Delete old image file if it exists
            if product.product_image:
                # Remove the file from the storage
                os.remove(os.path.join(settings.MEDIA_ROOT, str(product.product_image)))

            # Save the new image file
            product.product_image = product_image


       
        # Save the updated product
        product.save()
        
        return redirect('product_list')
    
    return render(request, 'admin/product_list.html', {'product': product})


def product_delete(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    
    categories=Categories.objects.all()
    context = {'categories':categories}
    return redirect('product_list')  

def admin_category(request):
    return render(request,'admin/admin_category.html')


def category_add(request):
    if request.method=='POST':
        category_name=request.POST.get('category_name')
        category= Categories(
            category_name=category_name
        )
        category.save()
        return redirect('category_add')
    categories = Categories.objects.all()  # Retrieve all categories
    return render(request, 'admin/admin_category.html', {'categories': categories})
    # return render(request,'admin/admin_category.html')
    
def category_delete(request,id):
    category=Categories.objects.get(id=id)
    category.delete()

    categories=Categories.objects.all()
    context = {'categories':categories}
    return redirect('category_add')

def category_update(request,id):
    category = get_object_or_404(Categories, id=id)

    if request.method=='POST':
        category_name = request.POST.get('category_name')

        category.category_name = category_name

        category.save()

        return redirect('category_add')
    return render(request, 'admin/admin_category.html', {'category': category})


def banner(request):
    banners = Banner.objects.all()
    context = {'banners':banners}
    return render(request,'admin/banner.html',context)



def banner_add(request):
    if request.method == 'POST':
        # Process the form submission
        banner_image = request.FILES.get('banner_image')
        banner = Banner(banner_image=banner_image)
        banner.save()
        return redirect('banner')
    else:
        # Display the form
        context = {}
        return render(request, 'admin/banner.html', context)


def banner_delete(request, id):
    if request.method == 'GET':
        banner = get_object_or_404(Banner, id=id)
        banner.delete()
        return redirect('banner')
    # else:
    #     # Handle GET request if needed
    #     # For example, you could render a confirmation template
    #     return HttpResponse("GET request not allowed for this view.")







