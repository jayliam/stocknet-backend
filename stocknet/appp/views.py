from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Service
from django.contrib.auth.models import User,auth
from django.contrib.auth import login
from products.models import Product
from clients.models import Client
from orders.models import SupplierOrder,ClientOrder
from suppliers.models import Supplier
from django.contrib import messages

def info(request):
    Ocount= request.user.clientorderlist.all().count()+request.user.supplierorderlist.all().count()
    list_products= request.user.productlist.all()
    OScount= request.user.supplierorderlist.all().count()
    OCcount= request.user.clientorderlist.all().count()

    OSPcount=list_order_suppliers= request.user.supplierorderlist.filter(Status='en attente').count()
    OCPcount=list_order_clients= request.user.clientorderlist.filter(Status='en attente').count()
    
    PendingOrdersCount=OCPcount + OSPcount
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
        "OScount": OScount,
        "OCcount": OCcount,
        "PendingOrdersCount": PendingOrdersCount,
        "repture_count": repture_count,
        "Ocount": Ocount,
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
            #Suppliers = suppliers,
            Category = category,
            Quantity = quantity
        )
        product.save()
        for s in suppliers:
            Sobj=Supplier.objects.get(Name=s)
            Sobj.save()
            product.Suppliers.add(Sobj)
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
    for s in obj.Suppliers.all():
        list_suppliers_obj.append(s.Name)
        print(list_suppliers_obj)
        print("*************************")
    
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
        #obj.Suppliers = suppliers
        obj.Category = category
        obj.Quantity = quantity
        for s in suppliers:
            Sobj=request.user.supplierlist.get(Name=s)
            #Sobj=Supplier.objects.get(Name=s)
            Sobj.save()
            obj.Suppliers.add(Sobj)


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



def PendingOrders_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')
    

    else:
        list_order_suppliers= request.user.supplierorderlist.filter(Status='en attente')
        list_order_clients= request.user.clientorderlist.filter(Status='en attente')

        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_order_clients" : list_order_clients,
        "list_order_suppliers" : list_order_suppliers
        }
        context.update(info(request))
        return render(request,"dashboard/order/pendingOrders_list.html",context)
def order_client_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            obj = ClientOrder.objects.get(id=int(i))
            obj.delete() 
        return redirect('order_client_list')      

    else:
        list_order_clients= request.user.clientorderlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_order_clients" : list_order_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_list.html",context)

def order_pending_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            obj = ClientOrder.objects.get(id=int(i))
            obj.delete() 
        return redirect('order_client_list')      

    else:
        list_order_clients= request.user.clientorderlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_order_clients" : list_order_clients
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_list.html",context)

def order_supplier_list(request):
    if request.method == 'POST':
        selectedlist = request.POST.getlist('selectedlist')

        for i in selectedlist:
            obj = SupplierOrder.objects.get(id=int(i))
            obj.delete() 
        return redirect('order_supplier_list')      

    else:
        list_order_suppliers= request.user.supplierorderlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount,
        "list_order_suppliers" : list_order_suppliers
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_list.html",context)


def order_client_create(request):
    if request.method == 'POST':
        
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        C = request.POST['client']
        Cobj = Client.objects.get(id=C)
        Cobj.save()


        Quantity = request.POST['quantity']
        Date = request.POST['date']
        Status = request.POST['status']
        error= False
        if not Product : 
            messages.info(request,'Le champ Product ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Client  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantity ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Status ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_client_create')
        print(Date)
        cOrder = ClientOrder(
            Quantity = Quantity,
            Date = Date,
            Status = Status
        )
        cOrder.save()
        
        request.user.clientorderlist.add(cOrder)
        Pobj.clientorderlist.add(cOrder)
        Cobj.clientorderlist.add(cOrder)

        messages.info(request,'Commande Ajouté')
        
        return redirect('order_client_list')

    else:
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
    }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_create.html",context)

def order_supplier_create(request):
    if request.method == 'POST':
        
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        S = request.POST['supplier']
        Sobj = Supplier.objects.get(id=S)
        Sobj.save()


        Quantity = request.POST['quantity']
        Date = request.POST['date']
        Status = request.POST['status']
        error= False
        if not Product : 
            messages.info(request,'Le champ Product ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Supplier  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantity ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Status ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_supplier_create')
        
        sOrder = SupplierOrder(
            Quantity = Quantity,
            Date = Date,
            Status = Status
        )
        sOrder.save()
        
        request.user.supplierorderlist.add(sOrder)
        Pobj.supplierorderlist.add(sOrder)
        Sobj.supplierorderlist.add(sOrder)

        messages.info(request,'Commande Ajouté')
        
        return redirect('order_supplier_list')

    else:
        productlist=request.user.productlist.all()
        supplierlist=request.user.supplierlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "supplierlist": supplierlist,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_create.html",context)


def order_supplier_edit(request,id):
    obj = get_object_or_404(SupplierOrder, id=id)
    if request.method == 'POST':
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        S = request.POST['supplier']
        Sobj = Supplier.objects.get(id=S)
        Sobj.save()


        Quantity = request.POST['quantity']
        Date = request.POST['date']
        Status = request.POST['status']
        error= False
        if not Product : 
            messages.info(request,'Le champ Produit ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Fournisseur  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantité ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Etat ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_supplier_edit',id)
        
        
        obj.Quantity = Quantity
        obj.Date = Date
        obj.Status = Status
        
        obj.save()
        
        request.user.supplierorderlist.add(obj)
        Pobj.supplierorderlist.add(obj)
        Sobj.supplierorderlist.add(obj)

        messages.info(request,'Commande Modifié')
        
        return redirect('order_supplier_list')

    else:
        
        productlist=request.user.productlist.all()
        supplierlist=request.user.supplierlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "supplierlist": supplierlist,
        "obj": obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_supplier_edit.html",context)

def order_client_edit(request,id):
    obj = get_object_or_404(ClientOrder, id=id)
    if request.method == 'POST':
        P = request.POST['product']
        Pobj = Product.objects.get(id=P)
        Pobj.save() 
        C = request.POST['client']
        Cobj = Client.objects.get(id=C)
        Cobj.save()


        Quantity = request.POST['quantity']
        Date = request.POST['date']
        Status = request.POST['status']
        error= False
        if not Product : 
            messages.info(request,'Le champ Product ne peut pas etre vide')
            error=True
        if not Client : 
            messages.info(request,'Le champ Supplier  ne peut pas etre vide')
            error=True
        if not Quantity : 
            messages.info(request,'Le champ Quantity ne peut pas etre vide')
            error=True
        if not Date : 
            messages.info(request,'Le champ Date ne peut pas etre vide')
            error=True
        if not Status : 
            messages.info(request,'Le champ Status ne peut pas etre vide')
            error=True
        if error:
            return redirect('order_client_edit',id)
        
        
        obj.Quantity = Quantity
        obj.Date = Date
        obj.Status = Status
        
        obj.save()
        
        request.user.clientorderlist.add(obj)
        Pobj.clientorderlist.add(obj)
        Cobj.clientorderlist.add(obj)

        messages.info(request,'Commande Modifié')
        
        return redirect('order_client_list')

    else:
        
        productlist=request.user.productlist.all()
        clientlist=request.user.clientlist.all()
        Pcount= request.user.productlist.all().count()
        Ccount= request.user.clientlist.all().count()
        Scount= request.user.supplierlist.all().count()
        context= {
        "productlist": productlist,
        "clientlist": clientlist,
        "obj": obj,
        "Pcount": Pcount,
        "Ccount": Ccount,
        "Scount": Scount
        }
        context.update(info(request))
        return render(request,"dashboard/order/order_client_edit.html",context)


def order_client_delete(request, id):
    obj=get_object_or_404(ClientOrder, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('order_client_list')
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
        return render(request,"dashboard/order/order_client_delete.html",context)
def order_client_deliver(request, id):
    order=get_object_or_404(ClientOrder, id=id)
    if order.Quantity > order.Product.Quantity:
        
        messages.warning(request,'Quantité insuffisante')
        return redirect('order_client_list')
    else:
        order.Product.Quantity=order.Product.Quantity-order.Quantity
        order.Product.save()
        order.Status='livré'
        order.save()
        messages.info(request,'Produit livré')
        return redirect('order_client_list')
       
def order_supplier_delete(request, id):
    obj=get_object_or_404(SupplierOrder, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('order_supplier_list')
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
        return render(request,"dashboard/order/order_supplier_delete.html",context)


def contact(request):
    return render(request,"contact.html",{})

def about(request):
    return render(request,"about.html",{})

def services(request):
    return render(request,"services.html",{})

def learnmore(request):
    return render(request,"learnmore.html",{})
