#!/bin/sh
crond -f -d 8 &
python3 manage.py runserver 0.0.0.0:8000
python3 manage.py collectstatic --no-input
