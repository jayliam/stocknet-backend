from django.db import models
from phone_field import PhoneField
from multiselectfield import MultiSelectField

TYPE_CHOICES  = (('Particulier', 'Particulier'),
               ('Entreprise', 'Entreprise'),
               )

# Create your models here.
class Client(models.Model):
    Type          = models.CharField(max_length=30, choices=TYPE_CHOICES, blank=False)
    Name          = models.CharField( max_length=30, blank=False)
    Phone         = PhoneField(blank=True, help_text='Contact phone number')
    Email         = models.EmailField( blank=True)
    Reference     = models.CharField(max_length=100)
    Adress        = models.CharField(max_length=100)
    Note          = models.TextField(blank=True, null=True)
    
    
    
