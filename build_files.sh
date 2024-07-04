#!/usr/bin/env bash

echo "Building Project Packages"
python3 -m pip install -r requirements.txt

echo "Migrating Database..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
