#!/usr/bin/env bash
set -e

echo "Waiting for postgres to connect ..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL is active"

python manage.py collectstatic
python manage.py migrate
python manage.py makemigrations

gunicorn truck_signs_designs.wsgi:application --bind 0.0.0.0:8000



echo "Postgresql migrations finished"

python manage.py runserver