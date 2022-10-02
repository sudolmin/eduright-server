#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn -k uvicorn.workers.UvicornWorker --env DJANGO_SETTINGS_MODULE=eduserver.settings --bind 0.0.0.0:8080 eduserver.wsgi