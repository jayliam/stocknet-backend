from django.db import models
from suppliers.models import Supplier
from multiselectfield import MultiSelectField

#THIS SHOULD BE IN VIEW SO THAT IT RELOADS WHEN ADDING NEW SUPPLIERS
#THIS
S_CHOICES=()
for s in Supplier.objects.all():
    S_CHOICES =  ((s.Name,s.Name),) + S_CHOICES 
#THIS



class Equipment(models.Model):
    Reference     = models.CharField(max_length=100)
    Manufacturer  = models.CharField(max_length=100)
    Description   = models.TextField(blank=True, null=True)
    PurchaseDate  = models.DateField()
    Category      = models.CharField(max_length=100)
    Suppliers     = MultiSelectField(choices=S_CHOICES)
    
    