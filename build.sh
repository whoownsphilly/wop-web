#!/usr/bin/env bash
# exit on error
set -o errexit

npm install
npm run build

poetry install

python manage.py collectstatic --no-input
python manage.py migrate
