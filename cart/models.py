from queue import PriorityQueue
from re import L
from django.db import models

from product.models import Product

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField(null=True, default=1) 
    
    
