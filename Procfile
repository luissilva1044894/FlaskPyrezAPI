web: gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
web: sh ./scripts/heroku.sh
bot: python bot_worker.py
#release: python wsgi.py db migrate

init: python wsgi.py db init
migrate: python wsgi.py db migrate
upgrade: python wsgi.py db upgrade
downgrade: python wsgi.py db downgrade

create_db: python wsgi.py create_db
drop_db: python wsgi.py drop_db
reset_db: python wsgi.py reset_db
update_db: python wsgi.py update_db
