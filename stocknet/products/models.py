from django.db import models
from suppliers.models import Supplier
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
#THIS SHOULD BE IN VIEW SO THAT IT RELOADS WHEN ADDING NEW SUPPLIERS
#THIS
S_CHOICES=()
for s in Supplier.objects.all():
    S_CHOICES =  ((s.Name,s.Name),) + S_CHOICES 
#THIS


class Product(models.Model):
    Title         = models.CharField(max_length=100)
    Description   = models.CharField(max_length=100, null = True)
    PurchasePrice = models.DecimalField(decimal_places=2, max_digits=20,default=0)
    SalesPrice    = models.DecimalField(decimal_places=2, max_digits=20,default=0,null=True)
    Reference     = models.CharField(max_length=100)
    Manufacturer  = models.CharField(max_length=100)
    #Suppliers     = models.ManyToManyField(Supplier)
    Suppliers     = MultiSelectField(choices=S_CHOICES)
    Category      = models.CharField(max_length=100)
    Quantity      = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name="productlist", null=True) # <--- added
    