from django.db import models

# Create your models here.

class Product(models.Model):
    Title         = models.CharField(max_length=100)
    Description   = models.TextField(blank=True, null=True)
    PurchasePrice = models.DecimalField(decimal_places=2, max_digits=20)
    SalesPrice    = models.DecimalField(decimal_places=2, max_digits=20)
    Reference     = models.CharField(max_length=100)
    Manufacturer  = models.CharField(max_length=100)
    suppliers     = []
    Category      = models.CharField(max_length=100)
    Quantity      = models.DecimalField(decimal_places=2, max_digits=20)
    
