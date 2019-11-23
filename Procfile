web: sh ./scripts/heroku.sh

web_asgi: -b 0.0.0.0:$PORT asgi:app -w 4 -k uvicorn.workers.UvicornWorker
web_wsgi: gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
web_hypercorn: hypercorn -b 0.0.0.0:${PORT} asgi:app
web_uvicorn: uvicorn asgi:app --host 0.0.0.0 --port $PORT

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
