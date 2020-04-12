from django.conf.urls import url, include
from . import views
from django.urls import path
urlpatterns = [
    path('norderc_list/', views.nOrderC_list, name='nOrderC_list'),
    path('norderc/create/', views.nOrderC_create, name='nOrderC_create'),

]