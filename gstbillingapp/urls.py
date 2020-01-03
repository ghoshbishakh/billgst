from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.customers, name='customers'),
    path('customersjson', views.customersjson, name='customersjson'),
    path('productsjson', views.productsjson, name='productsjson'),
    path('invoices', views.invoices, name='invoices'),
]