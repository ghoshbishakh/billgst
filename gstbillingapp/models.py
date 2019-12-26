from django.db import models

# Create your models here.


class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField(max_length=600, blank=True, null=True)
    customer_phone = models.CharField(max_length=14, blank=True, null=True)
    customer_gst = models.CharField(max_length=15, unique=True, blank=True, null=True)
    def __str__(self):
        return self.customer_name + " | " + self.customer_gst

class Invoice(models.Model):
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
