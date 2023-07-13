from django.db import models

# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    product_category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='images/products', default=None)
    product_description = models.CharField(max_length=200)
    product_price_per_kg = models.PositiveIntegerField()
    product_available_stock =  models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.product_name