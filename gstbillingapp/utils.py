import datetime
from .models import Product


def invoice_data_validator(invoice_data):
    
    # Validate Invoice Info ----------

    # invoice-number
    try:
        invoice_number = int(invoice_data['invoice-number'])
    except:
        print("Error: Incorrect Invoice Number")
        return "Error: Incorrect Invoice Number"

    # invoice date
    try:
        date_text = invoice_data['invoice-date']
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        print("Error: Incorrect Invoice Date")
        return "Error: Incorrect Invoice Date"

    # Validate Customer Data ---------

    # customer-name
    if len(invoice_data['customer-name']) < 1 or len(invoice_data['customer-name']) > 200:
        print("Error: Incorrect Customer Name")
        return "Error: Incorrect Customer Name"

    if len(invoice_data['customer-address']) > 600:
        print("Error: Incorrect Customer Address")
        return "Error: Incorrect Customer Address"

    if len(invoice_data['customer-phone']) > 14:
        print("Error: Incorrect Customer Phone")
        return "Error: Incorrect Customer Phone"
    if len(invoice_data['customer-gst']) != 15 and len(invoice_data['customer-gst']) != 0:
        print("Error: Incorrect Customer GST")
        return "Error: Incorrect Customer GST"
    return None


def invoice_data_processor(invoice_post_data):
    print(invoice_post_data)
    processed_invoice_data = {}

    processed_invoice_data['invoice_number'] = invoice_post_data['invoice-number']
    processed_invoice_data['invoice_date'] = invoice_post_data['invoice-date']

    processed_invoice_data['customer_name'] = invoice_post_data['customer-name']
    processed_invoice_data['customer_address'] = invoice_post_data['customer-address']
    processed_invoice_data['customer_phone'] = invoice_post_data['customer-phone']
    processed_invoice_data['customer_gst'] = invoice_post_data['customer-gst']

    processed_invoice_data['vehicle_number'] = invoice_post_data['vehicle-number']

    if 'igstcheck' in  invoice_post_data:
        processed_invoice_data['igstcheck'] = True
    else:
        processed_invoice_data['igstcheck'] = False

    processed_invoice_data['items'] = []
    processed_invoice_data['invoice_total_amt_without_gst'] = float(invoice_post_data['invoice-total-amt-without-gst'])
    processed_invoice_data['invoice_total_amt_sgst'] = float(invoice_post_data['invoice-total-amt-sgst'])
    processed_invoice_data['invoice_total_amt_cgst'] = float(invoice_post_data['invoice-total-amt-cgst'])
    processed_invoice_data['invoice_total_amt_igst'] = float(invoice_post_data['invoice-total-amt-igst'])
    processed_invoice_data['invoice_total_amt_with_gst'] = float(invoice_post_data['invoice-total-amt-with-gst'])


    invoice_post_data = dict(invoice_post_data)
    for idx, product in enumerate(invoice_post_data['invoice-product']):
        if product:
            print(idx, product)
            item_entry = {}
            item_entry['invoice_product'] = product
            item_entry['invoice_hsn'] = invoice_post_data['invoice-hsn'][idx]
            item_entry['invoice_unit'] = invoice_post_data['invoice-unit'][idx]
            item_entry['invoice_qty'] = int(invoice_post_data['invoice-qty'][idx])
            item_entry['invoice_rate_with_gst'] = float(invoice_post_data['invoice-rate-with-gst'][idx])
            item_entry['invoice_gst_percentage'] = float(invoice_post_data['invoice-gst-percentage'][idx])

            item_entry['invoice_rate_without_gst'] = float(invoice_post_data['invoice-rate-without-gst'][idx])
            item_entry['invoice_amt_without_gst'] = float(invoice_post_data['invoice-amt-without-gst'][idx])

            item_entry['invoice_amt_sgst'] = float(invoice_post_data['invoice-amt-sgst'][idx])
            item_entry['invoice_amt_cgst'] = float(invoice_post_data['invoice-amt-cgst'][idx])
            item_entry['invoice_amt_igst'] = float(invoice_post_data['invoice-amt-igst'][idx])
            item_entry['invoice_amt_with_gst'] = float(invoice_post_data['invoice-amt-with-gst'][idx])

            processed_invoice_data['items'].append(item_entry)

    print(processed_invoice_data)
    return processed_invoice_data


def update_products_from_invoice(invoice_data_processed):
    for item in invoice_data_processed['items']:
        print("ITEM:", item)
        if Product.objects.filter(product_name=item['invoice_product'],
                                  product_hsn=item['invoice_hsn'],
                                  product_unit=item['invoice_unit'],
                                  product_gst_percentage=item['invoice_gst_percentage']).exists():
            product = Product.objects.get(product_name=item['invoice_product'],
                                          product_hsn=item['invoice_hsn'],
                                          product_unit=item['invoice_unit'],
                                          product_gst_percentage=item['invoice_gst_percentage'])
        else:
            product = Product(product_name=item['invoice_product'],
                              product_hsn=item['invoice_hsn'],
                              product_unit=item['invoice_unit'],
                              product_gst_percentage=item['invoice_gst_percentage'])
        product.product_rate_with_gst = item['invoice_rate_with_gst']
        product.save()
