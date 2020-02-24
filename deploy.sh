git pull origin saas
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart uwsgi
