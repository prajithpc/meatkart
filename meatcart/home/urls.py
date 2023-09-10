from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products_home', views.products_home, name='products_home'),
    path('single_product/<str:id>', views.single_product, name='single_product'),
    path('products_home', views.products_home, name='products_home'),
    path('checkout', views.checkout, name='checkout'),
    path('success', views.success, name='success'),
    path('profile', views.profile, name='profile'),
    path('details', views.details, name='details'),
    path('address', views.address, name='address'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('addtowishlist', views.addtowishlist, name='addtowishlist'),
    path('deletefromwishlist/<int:product_id>/', views.deletefromwishlist, name='deletefromwishlist'),

    path('my_orders', views.my_orders, name='my_orders'),

]

