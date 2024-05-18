#!/bin/ash

echo "Apply Migrations"
python manage.py migrate

exec "$@"