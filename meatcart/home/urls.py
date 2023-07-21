from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products_home', views.products_home, name='products_home'),
    path('single_product/<str:id>', views.single_product, name='single_product'),
    path('products_home', views.products_home, name='products_home'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.success, name='success'),


   
]

