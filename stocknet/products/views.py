from django.shortcuts import render
from .models import Product
# Create your views here.
def productView(request):
    obj = Product.objects.get(id=1)
    context= {
        'object': obj 
    }
# OR
    # context ={
    #     'Title'         : obj.Title,
    #     'Description'   : obj.Description,
    #     'PurchasePrice' : obj.PurchasePrice,
    #     'SalesPrice'    : obj.SalesPrice,
    #     'Reference'     : obj.Reference,
    #     'Manufacturer'  : obj.Manufacturer,
    #     #'Suppliers'     : obj.Suppliers,
    #     'Category'      : obj.Category,
    #     'Quantity'      : obj.Quantity
    # }

    return render(request, "product/detail.html", context)