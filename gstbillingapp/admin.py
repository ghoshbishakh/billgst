from django.contrib import admin

# Register your models here.
from .models import Customer
from .models import Invoice
from .models import Product
from .models import UserProfile
from .models import BillingProfile

admin.site.register(UserProfile)
admin.site.register(BillingProfile)

admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Product)