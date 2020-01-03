#!/bin/bash
if [[ $DJANGO_SETTINGS_MODULE == "teleagh.settings.production" ]]
then
  echo "Starting gunicorn"
  gunicorn --bind 0.0.0.0:$PORT teleagh.wsgi
else
  echo "Starting developer server"
  python manage.py runserver 0.0.0.0:$PORT
fi