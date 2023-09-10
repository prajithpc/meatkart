from django.db import models
from django.contrib.auth.models import User 
from home.models import Product
from carts.models import *


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20,default='') 

    def __str__(self):
        return self.order_number
    

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),

    )


    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)

    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True,null=True, related_name='orders')
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=500)
    district = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    order_note = models.CharField(max_length=20)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=20,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    

class OrderProduct(models.Model):
    order_number = models.CharField(max_length=20, unique=True) 

    cart_item = models.ForeignKey(Cartitem, on_delete=models.CASCADE,default=None)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.order_number
    


