from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Service
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from products.models import Product
from clients.models import Client
from suppliers.models import Supplier
from django.contrib import messages

def info(request):
    list_products= request.user.productlist.all()
    repture_count=0
    stock_neg=0
    nbstock_neg=0
    notif=False
    for entry in list_products:
        if entry.Quantity == 0:
            repture_count=repture_count+ 1
        if entry.Quantity<0 :
            stock_neg=stock_neg+1
            nbstock_neg=nbstock_neg+entry.Quantity
    if ((repture_count > 0) or (nbstock_neg < 0)):
        notif=True
    context= {
        "stock_neg": stock_neg,
        "notif": notif,
        "repture_count": repture_count,
        "nbstock_neg": int(nbstock_neg)
    }
    return(context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else: 
        return render(request,"index.html",{})

def dashboard(request):

    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()

    
    list_products= request.user.productlist.all()
    repture_count=0
    stock_count=0
    stock_neg=0
    nbstock_neg=0
    notif=False
    for entry in list_products:
        if entry.Quantity>0:
            stock_count=stock_count+ entry.Quantity
        if entry.Quantity == 0:
            repture_count=repture_count+ 1
        if entry.Quantity<0 :
            stock_neg=stock_neg+1
            nbstock_neg=nbstock_neg+entry.Quantity
    if ((repture_count > 0) or (nbstock_neg < 0)):
        notif=True
    context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "stock_count": int(stock_count),
        "stock_neg": stock_neg,
        "notif": notif,
        "repture_count": repture_count,
        "nbstock_neg": int(nbstock_neg)
    }
    context.update(info(request))
    return render(request,"dashboard/dashboard.html",context)

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
                    
                    messages.info(request,'nom d utilisateur exist deja')
                else:    
                    if not password1:
                        request.user.username=username 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        pwd= request.user.password
                         
                        request.user.save()
                        user = auth.authenticate(username=username,password=pwd)
                        login(request,user)                        
                        
                        return redirect('account')
                        
                    else:
                        request.user.set_password(password1)
                        request.user.username=username 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        request.user.save()
                        user = auth.authenticate(username=username,password=password1)
                        login(request,user) 
                        return redirect('account')
                        
            else :  
                    
                    if not password1:

                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        pwd= request.user.password
                        usr= request.user.username
                        request.user.save()
                        user = auth.authenticate(username=usr,password=pwd)
                        login(request,user) 
                        return redirect('account')
                    else:
                        request.user.set_password(password1) 
                        request.user.first_name=first_name
                        request.user.last_name=last_name
                        usr= request.user.username
                        request.user.save()
                        user = auth.authenticate(username=usr,password=password1)
                        login(request,user) 
                        return redirect('account')
              
        else:
            messages.info(request,'les mots de passe ne correspondent pas')

        return redirect('account')
    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
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
        print(suppliers)
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
        #product.Suppliers.set(suppliers)
        request.user.productlist.add(product)
        messages.info(request,'Produit Ajouté')
        return redirect('product_list')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()

        list_suppliers= request.user.supplierlist.all()
        
        
        context = {
            "list_suppliers" : list_suppliers,
            "Pcount": Pcount,
            "Ccount": Ccount,
            "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/product/product_create.html",context)

def product_edit(request, id):
    obj = get_object_or_404(Product, id=id)
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()    
    list_suppliers= request.user.supplierlist.all()
    list_suppliers_obj=[]
    for s in obj.Suppliers:
        list_suppliers_obj.append(s)
    
    context = {
        "list_suppliers" : list_suppliers,
        "list_suppliers_obj" : list_suppliers_obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        
        "obj":obj
    }
    context.update(info(request))

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
            context.update(info(request))
            return render(request,"dashboard/product/product_edit.html",context)

        obj.Title = title
        obj.Description = description
        obj.PurchasePrice = purchaseprice
        obj.SalesPrice = salesprice
        obj.Reference = reference
        obj.Manufacturer = manufacturer
        obj.Suppliers = suppliers
        obj.Category = category
        obj.Quantity = quantity

        obj.save()
        messages.info(request,'Produit Sauvgardé')
        return redirect('product_list')

    else:
        context.update(info(request))
        return render(request,"dashboard/product/product_edit.html",context)

def product_list(request):

    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            #obj=get_object_or_404(Product, id=int(i))
            obj = Product.objects.get(id=int(i))
            obj.delete() 
        return redirect('product_list')      

    else:
        list_products= request.user.productlist.all()    
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()


        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_products" : list_products
        }
        context.update(info(request))
        return render(request,"dashboard/product/product_list.html",context)


def product_delete(request, id):
    obj=get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('product_list')
    else:    
        
        list_products= request.user.productlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count() 
        context= {
            "obj":obj,
            "Pcount": Pcount,
            "Ccount": Ccount,
            "Scount": Scount,
            "list_products" : list_products
        }
        context.update(info(request))
        return render(request,"dashboard/product/product_delete.html",context)


def reptureproduct_list(request):
    
    
    list_products= request.user.productlist.all()
   
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()

    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }
    context.update(info(request))
    return render(request,"dashboard/product/reptureroduct_list.html",context)
def negproduct_list(request):
    
    
    list_products= request.user.productlist.all()
    
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()


    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_products" : list_products
    }
    context.update(info(request))
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
            messages.info(request,'Le champ addresse ne peut pas etre vide')
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
        request.user.clientlist.add(client)
        return redirect('client_list')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/client/client_create.html",context)
def client_edit(request,id):
    obj = get_object_or_404(Client, id=id)
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "obj":obj
    }
    
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
            context.update(info(request))
            return render(request,"dashboard/client/client_edit.html",context)

        
        obj.Type = Type
        obj.Name = Name
        obj.Phone = Phone
        obj.Email = Email
        obj.Reference = Reference
        obj.Adress = Adress
        obj.Note = Note
        
        obj.save()
        messages.info(request,'Client modifié')
        return redirect('client_list')

    else:
        context.update(info(request))
        return render(request,"dashboard/client/client_edit.html",context)

def client_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            #obj=get_object_or_404(Product, id=int(i))
            obj = Client.objects.get(id=int(i))
            obj.delete() 
        return redirect('client_list')      

    else:
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/client/client_list.html",context)
def client_delete(request, id):
    obj=get_object_or_404(Client, id=id)


    if request.method == "POST":
        obj.delete()
        return redirect('client_list')
    else:
       
        list_clients= request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "obj":obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_clients" : list_clients
        }
        context.update(info(request))
        return render(request,"dashboard/client/client_delete.html",context)

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
            return redirect('supplier_create')

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
        request.user.supplierlist.add(supplier)  
        messages.info(request,'Fournisseur Ajouté')
        return redirect('supplier_list')

    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_create.html",context)
def supplier_edit(request,id=id):
    obj = get_object_or_404(Supplier, id=id)
    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()
    context= {
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "obj":obj
    }
    
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
            messages.info(request,'Le champ Adress ne peut pas etre vide')
            error=True
        if not Category : 
            messages.info(request,'Le champ Categorie ne peut pas etre vide')
            error=True

        if error:
            context.update(info(request))
            return render(request,"dashboard/supplier/supplier_edit.html",context)


        obj.Type = Type
        obj.Name = Name
        obj.Phone = Phone
        obj.Category = Category
        obj.Reference = Reference
        obj.Adress = Adress
        obj.Note = Note

        obj.save()
        messages.info(request,'Fournisseur Modifié')
        return redirect('supplier_list')

    else:
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_edit.html",context)

def supplier_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            #obj=get_object_or_404(Product, id=int(i))
            obj = Supplier.objects.get(id=int(i))
            obj.delete() 
        return redirect('supplier_list')      
    else:
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        list_suppliers= request.user.supplierlist.all()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_suppliers" : list_suppliers
        }
        context.update(info(request))
        return render(request,"dashboard/supplier/supplier_list.html",context)
def supplier_delete(request,id=id):
    obj=get_object_or_404(Supplier, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('supplier_list')    

    Pcount= request.user.productlist.all().count()
    Ccount= request.user.clientlist.all().count()
    Scount= request.user.supplierlist.all().count()
    suppliers = Supplier.objects.all()
    list_suppliers= request.user.supplierlist.all()
    context= {
    "obj":obj,
    "Pcount": Pcount,
    "Ccount": Ccount,
    "Scount": Scount,
    "list_suppliers" : list_suppliers
    }

    context.update(info(request))
    return render(request,"dashboard/supplier/supplier_delete.html",context)

def contact(request):
    return render(request,"contact.html",{})

def about(request):
    return render(request,"about.html",{})

def services(request):
    return render(request,"services.html",{})

def learnmore(request):
    return render(request,"learnmore.html",{})
