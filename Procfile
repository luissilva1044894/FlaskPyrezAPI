web: gunicorn -b 0.0.0.0:$PORT main:app --log-file=-
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
