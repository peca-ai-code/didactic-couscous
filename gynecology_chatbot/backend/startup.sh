#!/bin/bash
echo "Running database migrations..."
python3 manage.py migrate --noinput

echo "Creating guest user if needed..."
python3 create_guest_user.py || echo "Guest user already exists"

echo "Starting Gunicorn server..."
exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --preload gynecology_chatbot_project.wsgi:application
