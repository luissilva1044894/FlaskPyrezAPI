web: gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
worker: python bot_worker.py
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
create_db: python manage.py create_db
drop_db: python manage.py drop_db
reset_db: python manage.py reset_db
