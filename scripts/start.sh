#!/bin/sh
#Expects "export DJANGO_SETTINGS_MODULE=mysite.settings.local"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000