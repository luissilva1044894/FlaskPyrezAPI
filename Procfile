web1: gunicorn -b 0.0.0.0:$PORT main_old:app --log-file=-
web: gunicorn -b 0.0.0.0:$PORT main:app --log-file=- --preload --env FLASK_ENV=default --timeout 10
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
