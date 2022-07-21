from django.db import models

class Xarajat(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    user_id = models.PositiveBigIntegerField()
    comment = models.CharField(max_length=64)
    price = models.PositiveIntegerField(verbose_name="summa (UZS)", default=0)
    
    def __str__(self) -> str:
        return f"{self.comment} ({self.price})"
        