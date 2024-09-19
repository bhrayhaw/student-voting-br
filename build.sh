#!/bin/bash

set -e

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Navigate to the Django project directory
cd ./voter_system

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Make migrations
echo "Making migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Start Redis server (if Redis isn't already managed separately, e.g., via Docker or system service)
# echo "Starting Redis server..."
# redis-server --daemonize yes

# Start Celery worker (assumes the Celery configuration is already set up in your Django project)
echo "Starting Celery worker..."
celery -A voter_system worker --loglevel=info --detach

# Start Celery beat for scheduled tasks (optional)
echo "Starting Celery beat..."
celery -A voter_system beat --loglevel=info --detach

echo "File processing completed"

echo "Build completed successfully!"
