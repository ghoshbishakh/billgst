from django.forms import ModelForm
from .models import Customer

class CustomerForm(ModelForm):
     class Meta:
         model = Customer
         fields = ['customer_name', 'customer_address', 'customer_phone', 'customer_gst']