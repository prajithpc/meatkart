from django.urls import path
from . import views

urlpatterns = [
    path('handlelogin', views.handlelogin, name='handlelogin'),
    path('handlesignup', views.handlesignup, name='handlesignup'),
    path('handlelogout', views.handlelogout, name='handlelogout'),

    path('otp_verification', views.otp_verification, name='otp_verification'),
    path('verification', views.verification, name='verification'),

    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('reset_password', views.reset_password, name='reset_password'),

]
