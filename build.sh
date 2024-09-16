#!/bin/bash

pip install -r requirements.txt

cd ./voter_system && python manage.py collectstatic --noinput

cd ./voter_system && python manage.py makemigrations

cd ./voter_system && python manage.py migrate