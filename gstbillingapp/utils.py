import datetime


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
    processed_invoice_data['invoice-date'] = invoice_post_data['invoice-number']

    processed_invoice_data['customer-name'] = invoice_post_data['invoice-number']
    processed_invoice_data['customer-address'] = invoice_post_data['invoice-number']
    processed_invoice_data['customer-phone'] = invoice_post_data['invoice-number']
    processed_invoice_data['customer-gst'] = invoice_post_data['invoice-number']

    processed_invoice_data['items'] = []
    invoice_post_data = dict(invoice_post_data)
    for idx, product in enumerate(invoice_post_data['invoice-product']):
        if product:
            print(idx, product)
            item_entry = {}
            item_entry['invoice-product'] = product
            item_entry['invoice-hsn'] = invoice_post_data['invoice-product'][idx]
            item_entry['invoice-unit'] = invoice_post_data['invoice-unit'][idx]
            item_entry['invoice-qty'] = invoice_post_data['invoice-qty'][idx]
            item_entry['invoice-rate-with-gst'] = invoice_post_data['invoice-rate-with-gst'][idx]
            item_entry['invoice-gst-percentage'] = invoice_post_data['invoice-gst-percentage'][idx]
            processed_invoice_data['items'].append(item_entry)
    print(processed_invoice_data)
    return processed_invoice_data