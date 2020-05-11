from django.forms import ModelForm
from .models import Customer
from .models import Product
from .models import UserProfile
from .models import InventoryLog
from .models import BookLog


class CustomerForm(ModelForm):
     class Meta:
         model = Customer
         fields = ['customer_name', 'customer_address', 'customer_phone', 'customer_gst']


class ProductForm(ModelForm):
     class Meta:
         model = Product
         fields = ['product_name', 'product_hsn', 'product_unit', 'product_gst_percentage', 'product_rate_with_gst']


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['business_title'].required = True

    class Meta:
        model = UserProfile
        fields = ['business_title', 'business_address', 'business_email', 'business_phone', 'business_gst']


class InventoryLogForm(ModelForm):
    class Meta:
        model = InventoryLog
        fields = ['date', 'change', 'change_type', 'description']


class BookLogForm(ModelForm):
    class Meta:
        model = BookLog
        fields = ['date', 'change', 'change_type', 'description']