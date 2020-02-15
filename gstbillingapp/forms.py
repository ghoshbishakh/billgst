from django.forms import ModelForm
from .models import Customer
from .models import Product

class CustomerForm(ModelForm):
     class Meta:
         model = Customer
         fields = ['customer_name', 'customer_address', 'customer_phone', 'customer_gst']


class ProductForm(ModelForm):
     class Meta:
         model = Product
         fields = ['product_name', 'product_hsn', 'product_unit', 'product_gst_percentage', 'product_rate_with_gst']