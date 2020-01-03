from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('invoices', views.invoices, name='invoices'),
    path('customers', views.customers, name='customers'),
    path('products', views.products, name='products'),

    path('customersjson', views.customersjson, name='customersjson'),
    path('productsjson', views.productsjson, name='productsjson'),

    path('invoice/<int:invoice_id>', views.invoice_viewer, name='invoice_viewer'),
]