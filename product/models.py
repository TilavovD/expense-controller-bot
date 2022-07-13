from django.db import models

SALAD = "salad"
PLOV = "plov"
PRODUCT_CHOICES = (
    (SALAD, "salatlar"),
    (PLOV, "osh")
)

class Product(models.Model):
    product_photo = models.ImageField(upload_to ='uploads/')
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField(max_length=2048, null=True)
    type = models.CharField(max_length=16, choices=PRODUCT_CHOICES)
    