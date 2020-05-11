# BillGST

## Simplest GST invoicing app.

* Easily create invoices
* Manage inventory
* Keep books and track balances


## Getting Started

1. Clone the repository
2. Change `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` and `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` in `gstbilling/settings.py`
3.
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Clean Interface
![clean interface](https://github.com/ghoshbishakh/billgst/blob/master/gstbillingapp/static/gstbillingapp/images/screenshot_interface.png)

## Seamlessly add search products and customers
![seamless search](https://github.com/ghoshbishakh/billgst/blob/master/gstbillingapp/static/gstbillingapp/images.screenshot_search.png)

## Inventory Management
![inventory management](https://github.com/ghoshbishakh/billgst/blob/master/gstbillingapp/static/gstbillingapp/images/screenshot_inventory.png)

## Books Management
![books management](https://github.com/ghoshbishakh/billgst/blob/master/gstbillingapp/static/gstbillingapp/images/screenshot_books.png)
