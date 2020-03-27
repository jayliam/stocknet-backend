from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service
from django.contrib.auth.models import User
from products.models import Product
from clients.models import Client
from suppliers.models import Supplier

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else: 
        return render(request,"index.html",{})

def dashboard(request):
    Pcount= Product.objects.all().count()
    Ccount= Client.objects.all().count()
    Scount= Supplier.objects.all().count()
    contex= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
    return render(request,"dashboard/dashboard.html",contex)

def account(request):
    return render(request,"dashboard/account.html",{})

def product_create(request):
    return render(request,"dashboard/product/product_create.html",{})

def product_list(request):
    
    products = Product.objects.all()
    list_products= list(products)
    print(list_products)
    
    context = {
        "list_products" : list_products
    }
    return render(request,"dashboard/product/product_list.html",context)

def client_create(request):
    return render(request,"dashboard/client/client_create.html",{})

def client_list(request):
    clients = Client.objects.all()
    list_clients= list(clients)
    print(list_clients)
    
    context = {
        "list_clients" : list_clients
    }
    return render(request,"dashboard/client/client_list.html",context)

def supplier_create(request):
    return render(request,"dashboard/supplier/supplier_create.html",{})

def supplier_list(request):
    suppliers = Supplier.objects.all()
    list_suppliers= list(suppliers)
    print(list_suppliers)
    
    context = {
        "list_suppliers" : list_suppliers
    }
    return render(request,"dashboard/supplier/supplier_list.html",context)

def contact(request):
    return render(request,"contact.html",{})

def about(request):
    return render(request,"about.html",{})

def services(request):
    return render(request,"services.html",{})

def learnmore(request):
    return render(request,"learnmore.html",{})
