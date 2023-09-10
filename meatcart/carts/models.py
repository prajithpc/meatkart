from django.db import models

from home.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added =models.DateField(auto_now_add=True)



    def __str__(self):
        return self.cart_id
    


class Cartitem(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    # def sub_total(self):
    #     return self.product.product_price_per_kg * self.quantity

    def sub_total(self):
        product_price_per_kg = float(self.product.product_price_per_kg)
        product_discount = float(self.product.product_discount)

        # Calculate the discounted amount
        if product_discount is None or product_discount == 0:
            discounted_amount = product_price_per_kg
        else:
            discounted_amount = product_price_per_kg - (product_price_per_kg * product_discount / 100)

        return discounted_amount * self.quantity


    # def __str__(self):
    #     return self.product

    def __str__(self):
        return f"{self.product} - {self.quantity}"
