from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True ,null=True)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE ,null=True)
    product_image = models.ImageField(upload_to='images/products', default=None ,null=True)
    product_description = models.CharField(max_length=200 ,null=True)
    product_price_per_kg = models.PositiveIntegerField(null=True)
    product_available_stock =  models.DecimalField(max_digits=8, decimal_places=2, null=True)
    product_discount = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name
    

class Banner(models.Model):
    banner_image = models.ImageField(upload_to='images/products', default=None ,null=True)



class Wishitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product}"
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=500)
    district = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    postcodezip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.address_line_1}, {self.city}, {self.postcodezip}"