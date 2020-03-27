from django.urls import path,include
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('account/',views.account,name='account'),
    path('product_create/',views.product_create,name='product_create'),
    path('product_list/',views.product_list,name='product_list'),
    path('client_create/',views.client_create,name='client_create'),
    path('client_list/',views.client_list,name='client_list'),
    path('supplier_create/',views.supplier_create,name='supplier_create'),
    path('supplier_list/',views.supplier_list,name='supplier_list'),
    
]