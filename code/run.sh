#!/bin/bash
until ping -c1 $DB_HOST &>/dev/null; do :; done
python manage.py db upgrade
gunicorn -w 2 -b 0.0.0.0:5454 app:app
