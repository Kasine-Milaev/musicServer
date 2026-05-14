#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput

gunicorn musicService.asgi:application -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8080 --reload