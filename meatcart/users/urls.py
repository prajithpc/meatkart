from django.urls import path
from . import views

urlpatterns = [
    path('handlelogin', views.handlelogin, name='handlelogin'),
    path('handlesignup', views.handlesignup, name='handlesignup'),
    path('handlelogout', views.handlelogout, name='handlelogout'),


   
]
