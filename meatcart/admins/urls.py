from django.urls import path
from . import views



urlpatterns = [
    path('block/<int:id>/',views.user_block,name='user_block'),
    path('unblock/<int:id>/',views.user_unblock,name='user_unblock'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('adminhome', views.adminhome, name='adminhome'),
    path('user_list',views.user_list,name='user_list'),
    path('admin_category',views.admin_category,name='admin_category'),
    path('category_add',views.category_add,name='category_add'),
    path('category_delete/<str:id>',views.category_delete,name='category_delete'),
    path('category_update/<str:id>',views.category_update,name='category_update'),



    path('product_list',views.product_list,name='product_list'),
    path('product_add',views.product_add,name='product_add'),
    path('product_edit',views.product_edit,name='product_edit'),
    path('product_update/<str:id>',views.product_update,name='product_update'),
    path('product_delete/<str:id>',views.product_delete,name='product_delete'),




    
]
