from django.db import models
from phone_field import PhoneField
TYPE_CHOICES  = (('Particulier', 'Particulier'),
               ('Entreprise', 'Entreprise'),
               )


class Supplier(models.Model):
    Type          = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=False)    
    Name          = models.CharField(max_length=100) 
    Phone         = PhoneField(blank=True, help_text='Contact phone number')  
    Reference     = models.CharField(max_length=100)
    Category      = models.CharField(max_length=100)
    Adress        = models.CharField(max_length=100)
    Note          = models.TextField(blank=True, null=True)



    