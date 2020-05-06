web1: gunicorn -b 0.0.0.0:$PORT main_old:app --log-file=- --preload --env FLASK_ENV=default --timeout 10
web: gunicorn -b 0.0.0.0:$PORT main:app --log-file=-
#release: python manage.py create_db

downgrade: python manage.py db downgrade
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade

create_db: python manage.py create_db
drop_db: python manage.py drop_db
reset_db: python manage.py reset_db
