#!/bin/sh
#Expects "export DJANGO_SETTINGS_MODULE=mysite.settings.local"
#DJANGO_SETTINGS_MODULE=metabaron.settings.local sh scripts/start.sh 

python manage.py migrate
python manage.py create_superuser --noinput --password='12345' --username='admin' --email 'admin@fneh.com' --preserve
python manage.py loaddata --app lookup initial_data.json
python manage.py runserver 0.0.0.0:8000