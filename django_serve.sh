#!/bin/sh
poetry run pip install -r requirements.txt
poetry run python manage.py runserver ${1:-8000}
