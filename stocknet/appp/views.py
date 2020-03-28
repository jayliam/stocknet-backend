from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Service
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from products.models import Product
from clients.models import Client
from suppliers.models import Supplier
from django.contrib import messages

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

    products = Product.objects.all()
    list_products= list(products)
    repture_count=0
    stock_count=0
    stock_neg=0
    nbstock_neg=0
    for entry in list_products:
        if entry.Quantity>0:
            stock_count=stock_count+ entry.Quantity
        if entry.Quantity == 0:
            repture_count=repture_count+ 1
        if entry.Quantity<0 :
            stock_neg=stock_neg+1
            nbstock_neg=nbstock_neg+entry.Quantity

    contex= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "stock_count": int(stock_count),
        "stock_neg": stock_neg,
        "repture_count": repture_count,
        "nbstock_neg": int(nbstock_neg)
    }
    return render(request,"dashboard/dashboard.html",contex)

def account(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if(password1 == password2):
            if(request.user.username != username):
                if(User.objects.filter(username=username).exists()):
                    print('nom d utilisateur exist deja')
                    messages.info(request,'nom d utilisateur exist deja')
                else:    
                    if not password1:
                        request.user.username=username 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        pwd= request.user.password
                        print(request.user.username) 
                        request.user.save()
                        user = auth.authenticate(username=username,password=pwd)
                        login(request,user)                        
                        print('user updated')
                        return redirect('account')
                        
                    else:
                        request.user.set_password(password1)
                        request.user.username=username 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        print(request.user.username) 
                        request.user.save()
                        user = auth.authenticate(username=username,password=password1)
                        login(request,user) 
                        print('user updated')
                        return redirect('account')
                        
            else :  
                    
                    if not password1:

                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        pwd= request.user.password
                        usr= request.user.username
                        print(request.user.username)                       
                        request.user.save()
                        user = auth.authenticate(username=usr,password=pwd)
                        login(request,user) 
                        print('user created')
                        return redirect('account')
                    else:
                        request.user.set_password(password1) 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        usr= request.user.username
                        print(request.user.username) 
                        request.user.save()
                        user = auth.authenticate(username=usr,password=password1)
                        login(request,user) 
                        print('user updated')
                        return redirect('account')
              
        else:
            print('les mots de passe ne correspondent pas')
            messages.info(request,'les mots de passe ne correspondent pas')

        return redirect('account')
    else:
        Pcount= Product.objects.all().count()
        Ccount= Client.objects.all().count()
        Scount= Supplier.objects.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        return render(request,"dashboard/account.html",context)

def product_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        purchaseprice = request.POST['purchaseprice']
        salesprice = request.POST['salesprice']
        reference = request.POST['reference']
        manufacturer = request.POST['manufacturer']
        suppliers = request.POST.getlist('suppliers')
        category = request.POST['category']
        quantity = request.POST['quantity']

        error= False
        if not title : 
            messages.info(request,'Le champ titre ne peut pas etre vide')
            error=True
        if not purchaseprice : 
            messages.info(request,'Le champ Prix dachat ne peut pas etre vide')
            error=True
        if not salesprice : 
            messages.info(request,'Le champ Prix de vente ne peut pas etre vide')
            error=True
        if not reference : 
            messages.info(request,'Le champ reference ne peut pas etre vide')
            error=True
        if not manufacturer : 
            messages.info(request,'Le champ Fabricant ne peut pas etre vide')
            error=True
        if not category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True
        if not quantity : 
            messages.info(request,'Le champ quantité ne peut pas etre vide')
            error=True
        if not suppliers : 
            messages.info(request,'Le champ Fournisseurs  ne peut pas etre vide')
            error=True
        if error:
            return redirect('product_create')


        product = Product(
            Title=title, 
            Description=description,
            PurchasePrice=purchaseprice,
            SalesPrice = salesprice,
            Reference = reference,
            Manufacturer = manufacturer,
            Suppliers = suppliers,
            Category = category,
            Quantity = quantity
        )
        product.save()
        messages.info(request,'Produit Ajouté')
        return redirect('product_list')

    else:
        Pcount= Product.objects.all().count()
        Ccount= Client.objects.all().count()
        Scount= Supplier.objects.all().count() 

        suppliers = Supplier.objects.all()
        list_suppliers= list(suppliers)
        print(list_suppliers)
        
        context = {
            "list_suppliers" : list_suppliers,
            "Pcount": Pcount,
            "Ccount": Ccount,
            "Scount": Scount
        }
        return render(request,"dashboard/product/product_create.html",context)

def product_list(request):
    
    products = Product.objects.all()
    list_products= list(products)
    print(list_products)
    Pcount= Product.objects.all().count()
    Ccount= Client.objects.all().count()
    Scount= Supplier.objects.all().count()
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }

    return render(request,"dashboard/product/product_list.html",context)

def reptureproduct_list(request):
    
    products = Product.objects.all()
    list_products= list(products)
    print(list_products)
    Pcount= Product.objects.all().count()
    Ccount= Client.objects.all().count()
    Scount= Supplier.objects.all().count()


    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }

    return render(request,"dashboard/product/reptureroduct_list.html",context)
def negproduct_list(request):
    
    products = Product.objects.all()
    list_products= list(products)
    print(list_products)
    Pcount= Product.objects.all().count()
    Ccount= Client.objects.all().count()
    Scount= Supplier.objects.all().count()


    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }

    return render(request,"dashboard/product/negproduct_list.html",context)

def client_create(request):
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Email = request.POST['email']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if error:
            return redirect('client_create')

        client = Client(
            Type = Type,
            Name = Name,
            Phone = Phone,
            Email = Email,
            Reference = Reference,
            Adress = Adress,
            Note = Note
        )
        client.save()
        messages.info(request,'Client Ajouté')
        return redirect('client_list')

    else:
        Pcount= Product.objects.all().count()
        Ccount= Client.objects.all().count()
        Scount= Supplier.objects.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        return render(request,"dashboard/client/client_create.html",context)

def client_list(request):
    clients = Client.objects.all()
    list_clients= list(clients)
    print(list_clients)
    

    Pcount= Product.objects.all().count()
    Ccount= Client.objects.all().count()
    Scount= Supplier.objects.all().count()
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_clients" : list_clients
    }
    return render(request,"dashboard/client/client_list.html",context)

def supplier_create(request):
    if request.method == 'POST':
        Type = request.POST['type']
        Name = request.POST['name']
        Phone = request.POST['phone']
        Category = request.POST['category']
        Reference = request.POST['reference']
        Adress = request.POST['adress']
        Note = request.POST['note']
        
        error= False
        if not Name : 
            messages.info(request,'Le champ Nom  ne peut pas etre vide')
            error=True
        if not Phone : 
            messages.info(request,'Le champ Numero telephone  ne peut pas etre vide')
            error=True
        if not Reference : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Adress : 
            messages.info(request,'Le champ Reference ne peut pas etre vide')
            error=True
        if not Category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True

        if error:
            return redirect('client_create')

        supplier = Supplier(
            Type = Type,
            Name = Name,
            Phone = Phone,
            Category = Category,
            Reference = Reference,
            Adress = Adress,
            Note = Note
        )
        supplier.save()
        messages.info(request,'Client Ajouté')
        return redirect('supplier_list')

    else:
        Pcount= Product.objects.all().count()
        Ccount= Client.objects.all().count()
        Scount= Supplier.objects.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        return render(request,"dashboard/supplier/supplier_create.html",context)

def supplier_list(request):
    Pcount= Product.objects.all().count()
    Ccount= Client.objects.all().count()
    Scount= Supplier.objects.all().count()
    suppliers = Supplier.objects.all()
    list_suppliers= list(suppliers)
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
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
