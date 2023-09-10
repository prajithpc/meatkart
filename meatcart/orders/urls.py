from django.urls import path
from . import views
# app_name = 'orders'
urlpatterns =[
    path('place_order/',views.place_order,name='place_order'),
    path('orders/orderlist/',views.orderlist,name='orderlist'),

    path('orders/update_order_status/<int:id>/', views.update_order_status, name='update_order_status'),


    path('order_detail/<str:order_id>/', views.order_detail, name='order_detail'),

    path('saved_addresses/', views.saved_addresses, name='saved_addresses'),

]