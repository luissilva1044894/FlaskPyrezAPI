#!/bin/bash
python3 manage.py db upgrade

python manage.py wsgi:app --env FLASK_ENV=default --preload -h 0.0.0.0 -p ${PORT:-8000}
