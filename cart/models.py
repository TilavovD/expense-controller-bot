from math import prod
from django.db import models

from product.models import Product

class Cart(models.Model):
    user_id = models.PositiveBigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField(null=True, default=1) 
    
    def get_total_price(self, product):
        return product.quantity*product.product.price
    
    
