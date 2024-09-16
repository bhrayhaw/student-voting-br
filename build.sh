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

echo "Build completed successfully!"