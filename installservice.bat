sc stop "GSTBILLING"
sc delete "GSTBILLING"
sc create "GSTBILLING" start= auto displayname= "GST Billing Service" binpath= "%~dp0\python-3.8.1-embed-amd64\python.exe %~dp0\manage.py runserver"
sc start "GSTBILLING"
