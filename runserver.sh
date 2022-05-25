#!/bin/sh

python manage.py collectstatic --no-input --clear
python manage.py migrate
python manage.py loaddata users websites settings states
gunicorn FreezeMe.wsgi --bind=0.0.0.0:80