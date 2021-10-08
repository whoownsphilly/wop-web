#!/bin/sh
poetry run pip install -r requirements.txt
poetry run python manage.py runserver ${DJANGO_PORT:-8000}
