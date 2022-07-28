#!/usr/bin/env bash

python manage.py migrate

gunicorn --bind :"$PORT" \
         -k gevent \
         --timeout 30 \
         --graceful-timeout 30 \
         --workers 5 \
         --worker-connections 100 \
         --max-requests 5000 \
         --max-requests-jitter 50 \
         wsgi:application
