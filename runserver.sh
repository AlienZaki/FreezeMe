#!/bin/sh

python manage.py collectstatic --no-input --clear
python manage.py migrate
python manage.py loaddata users websites settings clients requirements submissions states settings
gunicorn FreezeMe.wsgi --bind=0.0.0.0:80