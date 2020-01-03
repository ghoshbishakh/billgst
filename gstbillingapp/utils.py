import datetime
from .models import Product


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


def invoice_data_processor(invoice_post_data):
    print(invoice_post_data)
    processed_invoice_data = {}

    processed_invoice_data['invoice-number'] = invoice_post_data['invoice-number']
    processed_invoice_data['invoice-date'] = invoice_post_data['invoice-date']

    processed_invoice_data['customer-name'] = invoice_post_data['customer-name']
    processed_invoice_data['customer-address'] = invoice_post_data['customer-address']
    processed_invoice_data['customer-phone'] = invoice_post_data['customer-phone']
    processed_invoice_data['customer-gst'] = invoice_post_data['customer-gst']

    processed_invoice_data['vehicle-number'] = invoice_post_data['vehicle-number']

    processed_invoice_data['items'] = []
    invoice_post_data = dict(invoice_post_data)
    for idx, product in enumerate(invoice_post_data['invoice-product']):
        if product:
            print(idx, product)
            item_entry = {}
            item_entry['invoice-product'] = product
            item_entry['invoice-hsn'] = invoice_post_data['invoice-hsn'][idx]
            item_entry['invoice-unit'] = invoice_post_data['invoice-unit'][idx]
            item_entry['invoice-qty'] = invoice_post_data['invoice-qty'][idx]
            item_entry['invoice-rate-with-gst'] = invoice_post_data['invoice-rate-with-gst'][idx]
            item_entry['invoice-gst-percentage'] = invoice_post_data['invoice-gst-percentage'][idx]
            processed_invoice_data['items'].append(item_entry)
    print(processed_invoice_data)
    return processed_invoice_data


def update_products_from_invoice(invoice_data_processed):
    for item in invoice_data_processed['items']:
        print("ITEM:", item)
        if Product.objects.filter(product_name=item['invoice-product'],
                                  product_hsn=item['invoice-hsn'],
                                  product_unit=item['invoice-unit'],
                                  product_gst_percentage=item['invoice-gst-percentage']).exists():
            product = Product.objects.get(product_name=item['invoice-product'],
                                          product_hsn=item['invoice-hsn'],
                                          product_unit=item['invoice-unit'],
                                          product_gst_percentage=item['invoice-gst-percentage'])
        else:
            product = Product(product_name=item['invoice-product'],
                              product_hsn=item['invoice-hsn'],
                              product_unit=item['invoice-unit'],
                              product_gst_percentage=item['invoice-gst-percentage'])
        product.product_rate_with_gst = item['invoice-rate-with-gst']
        product.save()
