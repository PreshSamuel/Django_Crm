#! /bin/sh

python3 manage.py migrate
python manage.py collectstatic --no-input
gunicorn config.wsgi:application