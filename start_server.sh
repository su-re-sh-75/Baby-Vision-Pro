#!/bin/zsh

echo "Starting Django development server..."
python manage.py runserver &

echo "Starting Celery worker..."
celery -A Baby_app worker --loglevel=info &

echo "Starting Celery beat..."
celery -A Baby_app  beat --loglevel=info &

wait
