from django.db import models

# Create your models here.


class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField(max_length=600)
    customer_phone = models.CharField(max_length=14)
    customer_gst = models.CharField(max_length=15)
