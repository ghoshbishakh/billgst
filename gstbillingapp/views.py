import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer
from .models import Invoice

def invoice_data_validator(invoice_data):
    
    # Validate Invoice Info ----------

    # invoice-number
    try:
        invoice_number = int(invoice_data['invoice-number'])
    except:
        print("Error: Incorrect Invoice Number")
        return False

    # invoice date
    try:
        date_text = invoice_data['invoice-date']
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Error: Incorrect Invoice Date")
        return False

    # Validate Customer Data ---------

    # customer-name
    if len(invoice_data['customer-name']) < 1 or len(invoice_data['customer-name']) > 200:
        print("Error: Incorrect Customer Name")
        return False

    if len(invoice_data['customer-address']) > 600:
        print("Error: Incorrect Customer Address")
        return False

    if len(invoice_data['customer-phone']) > 14:
        print("Error: Incorrect Customer Phone")
        return False
    if len(invoice_data['customer-gst']) != 15 and len(invoice_data['customer-gst']) != 0:
        print("Error: Incorrect Customer GST")
        return False
    return True

# Create your views here.
def index(request):
    context = {}
    if request.method == 'POST':
        print("POST received - Invoice Data")

        invoice_data = request.POST
        if not invoice_data_validator(invoice_data):
            return render(request, 'gstbillingapp/index.html', context)

        # valid invoice data
        print("Valid Invoice Data")
        # save customer
        customer = None
        if len(invoice_data['customer-gst']) == 15:
            if Customer.objects.filter(customer_gst=invoice_data['customer-gst']).exists():
                customer = Customer.objects.get(customer_gst=invoice_data['customer-gst'])
        if not customer:
            customer = Customer(customer_name=invoice_data['customer-name'],
                customer_address=invoice_data['customer-address'],
                customer_phone=invoice_data['customer-phone'],
                customer_gst=invoice_data['customer-gst'])
            customer.save()

        # save invoice
        new_invoice = Invoice(invoice_number=int(invoice_data['invoice-number']), invoice_date=datetime.datetime.strptime(invoice_data['invoice-date'], '%Y-%m-%d'), invoice_customer=customer, invoice_json=json.dumps(request.POST))
        new_invoice.save()
        print("INVOICE SAVED")
        return render(request, 'gstbillingapp/index.html', context)
    return render(request, 'gstbillingapp/index.html', context)


def customers(request):
    context = {}
    context['customers'] = Customer.objects.all()
    return render(request, 'gstbillingapp/customers.html', context)