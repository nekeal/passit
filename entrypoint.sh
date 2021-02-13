#!/bin/bash
if [[ $DJANGO_SETTINGS_MODULE == "passit.settings.production" ]]
then
  echo "Starting gunicorn"
  gunicorn --bind 0.0.0.0:$PORT passit.wsgi
else
  echo "Starting developer server"
  python manage.py runserver 0.0.0.0:$PORT
fi
