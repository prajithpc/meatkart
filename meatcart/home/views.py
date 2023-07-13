from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404


# Create your views here.


def index(request):
    return render(request, 'home/home.html')
    

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

# def error_404(request,exception):
#     return render(request,'404.html')


# def single_product(request,id):
#     products = Product.objects.get(id=id)
#     product_images = ProductImages.objects.filter(name=products)
#     colors = ProductImages.objects.filter(name=products).values_list('colors__color_name', flat=True).distinct()
#     selected_color = request.GET.get('color')
#     selected_varient = request.GET.get('size')
#     product_varients = ProductVarient.objects.filter(name=products)
#     for i in range(0,len(product_images)):
#         product_images[i].str_colors = str(product_images[i].colors)
#     if not selected_color:
#         selected_color = product_images[0].str_colors
#     varients = ProductVarient.objects.filter(name = products)
#     str_varients = []
#     for i in range(0, len(varients)):
#         if (str(varients[i].colors) == selected_color):
#             str_varients.append(str(varients[i].size)) 

#     if not selected_varient:
#         selected_varient = str_varients[0]
#     the_color = selected_color
#     the_size = int(selected_varient)
#     my_varient = None
#     for i in range(0, len(product_varients)):
#         if product_varients[i].colors.colors.color_name == the_color and product_varients[i].size.size_number == the_size:
#             my_varient = product_varients[i]
#             break    
#     context = {
#         'products':products, 
#         'product_images':product_images,
#         'varients':varients,
#         'str_varients':str_varients,
#         'colors' : colors,
#         'selected_color': selected_color,
#         'selected_varient': selected_varient,
#         'my_varient_id': str(my_varient.id),
#         }
#     return render(request,'home/product-single.html', context)