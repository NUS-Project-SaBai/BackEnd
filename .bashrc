#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install pipenv
pipenv --python 3.12
pipenv shell
pipenv install
pipenv run start