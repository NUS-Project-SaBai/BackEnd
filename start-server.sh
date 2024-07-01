#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py get_auth0_users
python manage.py runserver