web: gunicorn -b 0.0.0.0:$PORT web:app --log-file=- --env FLASK_ENV=default 
web: gunicorn -b 0.0.0.0:$PORT wsgi:application --log-file=- --env FLASK_ENV=default
web: python wsgi.py
worker: python bot_worker.py
