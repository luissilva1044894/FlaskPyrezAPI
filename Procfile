web: gunicorn -b 0.0.0.0:$PORT web:app --log-file=- --env WEB_CONCURRENCY=3
web: gunicorn -b 0.0.0.0:$PORT wsgi:application --env FLASK_ENV=default --preload
worker: python bot_worker.py
