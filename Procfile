web: gunicorn -b 0.0.0.0:$PORT web:app --log-file=- --env FLASK_ENV=default 
web: python manage.py runserver
web: gunicorn -b 0.0.0.0:$PORT wsgi:application --env WEB_CONCURRENCY=3 --preload
worker: python bot_worker.py
