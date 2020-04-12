from django import forms
from .models import nOrderS,nOrderC,nSupplierOrder,nClientOrder
class nOrderCForm(forms.ModelForm):
    class Meta:
        model = nOrderC
        fields = ('Product', 'Quantity',  )

            