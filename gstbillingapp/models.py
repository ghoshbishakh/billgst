from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ========================== Saas Data models ==================================

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    business_title = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(max_length=400, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    business_phone = models.CharField(max_length=20, blank=True, null=True)
    business_gst = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Plan(models.Model):
    plan_name = models.TextField(max_length=20, blank=True, null=True)
    plan_value = models.IntegerField(blank=True, null=True)
    monthly_invoice_limit = models.IntegerField(blank=True, null=True)


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.SET_NULL)
    plan_start_date = models.DateField(blank=True, null=True)
    plan_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# ======================= Invoice Data models =================================

class Customer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField(max_length=600, blank=True, null=True)
    customer_phone = models.CharField(max_length=14, blank=True, null=True)
    customer_gst = models.CharField(max_length=15, unique=True, blank=True, null=True)
    def __str__(self):
        return self.customer_name


class Invoice(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    invoice_number = models.IntegerField()
    invoice_date = models.DateField()
    invoice_customer = models.ForeignKey(
        'Customer',
        on_delete=models.SET_NULL,
        null=True
    )
    invoice_json = models.TextField()
    def __str__(self):
        return str(self.invoice_number) + " | " + str(self.invoice_date)


class Product(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=200)
    product_hsn = models.CharField(max_length=50)
    product_unit = models.CharField(max_length=50)
    product_gst_percentage = models.FloatField()
    product_rate_with_gst = models.FloatField()
    def __str__(self):
        return str(self.product_name)
