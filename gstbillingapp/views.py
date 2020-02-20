import datetime
import json
import num2words

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Max

from django.contrib.auth.decorators import login_required


from .models import Customer
from .models import Invoice
from .models import Product
from .models import UserProfile

from .utils import invoice_data_validator
from .utils import invoice_data_processor
from .utils import update_products_from_invoice

from .forms import CustomerForm
from .forms import ProductForm
from .forms import UserProfileForm

# Create your views here.
@login_required
def index(request):
    context = {}
    context['default_invoice_number'] = Invoice.objects.filter(user=request.user).aggregate(Max('invoice_number'))['invoice_number__max']
    if not context['default_invoice_number']:
        context['default_invoice_number'] = 1
    else:
        context['default_invoice_number'] += 1

    context['default_invoice_date'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')

    if request.method == 'POST':
        print("POST received - Invoice Data")

        invoice_data = request.POST

        validation_error = invoice_data_validator(invoice_data)
        if validation_error:
            context["validation_error"] = validation_error
            return render(request, 'gstbillingapp/index.html', context)

        # valid invoice data
        print("Valid Invoice Data")

        invoice_data_processed = invoice_data_processor(invoice_data)
        # save customer
        customer = None
        if len(invoice_data['customer-gst']) == 15:
            if Customer.objects.filter(user=request.user, customer_gst=invoice_data['customer-gst']).exists():
                customer = Customer.objects.get(user=request.user, customer_gst=invoice_data['customer-gst'])
        if not customer:
            customer = Customer(user=request.user,
                customer_name=invoice_data['customer-name'],
                customer_address=invoice_data['customer-address'],
                customer_phone=invoice_data['customer-phone'],
                customer_gst=invoice_data['customer-gst'])
            customer.save()

        # save product
        update_products_from_invoice(invoice_data_processed, request)


        # save invoice
        invoice_data_processed_json = json.dumps(invoice_data_processed)
        new_invoice = Invoice(user=request.user,
                              invoice_number=int(invoice_data['invoice-number']),
                              invoice_date=datetime.datetime.strptime(invoice_data['invoice-date'], '%Y-%m-%d'),
                              invoice_customer=customer, invoice_json=invoice_data_processed_json)
        new_invoice.save()
        print("INVOICE SAVED")
        return redirect('invoice_viewer', invoice_id=new_invoice.id)

    return render(request, 'gstbillingapp/index.html', context)


@login_required
def customers(request):
    context = {}
    context['customers'] = Customer.objects.filter(user=request.user)
    return render(request, 'gstbillingapp/customers.html', context)


@login_required
def products(request):
    context = {}
    context['products'] = Product.objects.filter(user=request.user)
    return render(request, 'gstbillingapp/products.html', context)


@login_required
def customersjson(request):
    customers = list(Customer.objects.filter(user=request.user).values())
    return JsonResponse(customers, safe=False)


@login_required
def productsjson(request):
    products = list(Product.objects.filter(user=request.user).values())
    return JsonResponse(products, safe=False)


@login_required
def invoices(request):
    context = {}
    context['invoices'] = Invoice.objects.filter(user=request.user).order_by('-id')
    return render(request, 'gstbillingapp/invoices.html', context)


@login_required
def invoice_viewer(request, invoice_id):
    invoice_obj = get_object_or_404(Invoice, user=request.user, id=invoice_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {}
    context['invoice'] = invoice_obj
    context['invoice_data'] = json.loads(invoice_obj.invoice_json)
    print(context['invoice_data'])
    context['currency'] = "₹"
    context['total_in_words'] = num2words.num2words(int(context['invoice_data']['invoice_total_amt_with_gst']), lang='en_IN').title()
    context['user_profile'] = user_profile
    return render(request, 'gstbillingapp/invoice_printer.html', context)


@login_required
def customer_edit(request, customer_id):
    customer_obj = get_object_or_404(Customer, user=request.user, id=customer_id)
    if request.method == "POST":
        customer_form = CustomerForm(request.POST, instance=customer_obj)
        if customer_form.is_valid():
            new_customer = customer_form.save()
            return redirect('customers')
    context = {}
    context['customer_form'] = CustomerForm(instance=customer_obj)
    return render(request, 'gstbillingapp/customer_edit.html', context)


@login_required
def customer_delete(request):
    if request.method == "POST":
        customer_id = request.POST["customer_id"]
        customer_obj = get_object_or_404(Customer, user=request.user, id=customer_id)
        customer_obj.delete()
    return redirect('customers')


@login_required
def customer_add(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST)
        new_customer = customer_form.save(commit=False)
        new_customer.user = request.user
        new_customer.save()
        return redirect('customers')
    context = {}
    context['customer_form'] = CustomerForm()
    return render(request, 'gstbillingapp/customer_edit.html', context)


@login_required
def product_edit(request, product_id):
    product_obj = get_object_or_404(Product, user=request.user, id=product_id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product_obj)
        if product_form.is_valid():
            new_product = product_form.save()
            return redirect('products')
    context = {}
    context['product_form'] = ProductForm(instance=product_obj)
    return render(request, 'gstbillingapp/product_edit.html', context)


@login_required
def product_add(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('products')
    context = {}
    context['product_form'] = ProductForm()
    return render(request, 'gstbillingapp/product_edit.html', context)


@login_required
def product_delete(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        product_obj = get_object_or_404(Product, user=request.user, id=product_id)
        product_obj.delete()
    return redirect('products')


@login_required
def user_profile_edit(request):
    context = {}
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context['user_profile_form'] = UserProfileForm(instance=user_profile)
    
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_profile_form.save()
        return redirect('user_profile')
    return render(request, 'gstbillingapp/user_profile_edit.html', context)


@login_required
def user_profile(request):
    context = {}
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context['user_profile'] = user_profile
    return render(request, 'gstbillingapp/user_profile.html', context)


def login_view(request):
    context = {}
    return render(request, 'gstbillingapp/login.html', context)