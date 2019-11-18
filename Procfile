web: gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
worker: python bot_worker.py
