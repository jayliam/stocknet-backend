from django import forms
from .models import nOrderS,nOrderC,nSupplierOrder,nClientOrder
class nOrderCForm(forms.ModelForm):
    class Meta:
        model = nOrderC
        fields = ('Product', 'Quantity',  )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.kwargs.get('user')
        if user:
            self.fields['Product'].queryset = user.product_set.all()


class nClientOrderForm(forms.ModelForm):
    class Meta:
        model = nClientOrder
        fields = ('Client', 'Date',  )

            