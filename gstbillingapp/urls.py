from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('invoices/new', views.invoice_create, name='invoice_create'),
    path('invoices/delete', views.invoice_delete, name='invoice_delete'),

    path('login', views.login_view, name='login_view'),
    path('signup', views.signup_view, name='signup_view'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('invoices', views.invoices, name='invoices'),
    path('invoice/<int:invoice_id>', views.invoice_viewer, name='invoice_viewer'),

    path('customers', views.customers, name='customers'),
    path('customers/add', views.customer_add, name='customer_add'),
    path('customers/edit/<int:customer_id>', views.customer_edit, name='customer_edit'),
    path('customers/delete', views.customer_delete, name='customer_delete'),
    path('customersjson', views.customersjson, name='customersjson'),

    path('products', views.products, name='products'),
    path('products/add', views.product_add, name='product_add'),
    path('products/edit/<int:product_id>', views.product_edit, name='product_edit'),
    path('products/delete', views.product_delete, name='product_delete'),
    path('productsjson', views.productsjson, name='productsjson'),

    path('inventory', views.inventory, name='inventory'),
    path('inventory/<int:inventory_id>', views.inventory_logs, name='inventory_logs'),
    path('inventory/<int:inventory_id>/addupdate', views.inventory_logs_add, name='inventory_logs_add'),

    path('books', views.books, name='books'),
    path('books/<int:book_id>', views.book_logs, name='book_logs'),
    path('books/<int:book_id>/addupdate', views.book_logs_add, name='book_logs_add'),


    path('profile', views.user_profile, name='user_profile'),
    path('profile/edit', views.user_profile_edit, name='user_profile_edit'),


]