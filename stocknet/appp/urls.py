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
    path('product/<int:id>/delete/',views.product_delete,name='product_delete'),
    path('client/<int:id>/delete/',views.client_delete,name='client_delete'),
    path('client/<int:id>/edit/',views.client_edit,name='client_edit'),
    path('supplier/<int:id>/delete/',views.supplier_delete,name='supplier_delete'),
    path('supplier/<int:id>/edit/',views.supplier_edit,name='supplier_edit'),
    path('product/<int:id>/edit/',views.product_edit,name='product_edit'),
    path('product_list/',views.product_list,name='product_list'),
    path('negproduct_list/',views.negproduct_list,name='negproduct_list'),
    path('reptureproduct_list/',views.reptureproduct_list,name='reptureproduct_list'),
    path('client_create/',views.client_create,name='client_create'),
    path('client_list/',views.client_list,name='client_list'),
    path('supplier_create/',views.supplier_create,name='supplier_create'),
    path('supplier_list/',views.supplier_list,name='supplier_list'),
    
]