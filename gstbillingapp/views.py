import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Max

from .models import Customer
from .models import Invoice
from .models import Product

from .utils import invoice_data_validator
from .utils import invoice_data_processor
from .utils import update_products_from_invoice

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

        invoice_data_processed = invoice_data_processor(invoice_data)
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

        # save product
        update_products_from_invoice(invoice_data_processed)


        # save invoice
        new_invoice = Invoice(invoice_number=int(invoice_data['invoice-number']), invoice_date=datetime.datetime.strptime(invoice_data['invoice-date'], '%Y-%m-%d'), invoice_customer=customer, invoice_json=invoice_data_processed)
        new_invoice.save()
        print("INVOICE SAVED")
        return render(request, 'gstbillingapp/index.html', context)


    context['default_invoice_number'] = Invoice.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
    if not context['default_invoice_number']:
        context['default_invoice_number'] = 1
    else:
        context['default_invoice_number'] += 1

    context['default_invoice_date'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    return render(request, 'gstbillingapp/index.html', context)


def customers(request):
    context = {}
    context['customers'] = Customer.objects.all()
    return render(request, 'gstbillingapp/customers.html', context)


def customersjson(request):
    customers = list(Customer.objects.values())
    return JsonResponse(customers, safe=False)


def productsjson(request):
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False)


def invoices(request):
    context = {}
    context['invoices'] = Invoice.objects.all().order_by('-id')
    return render(request, 'gstbillingapp/invoices.html', context)