web: gunicorn app:app --log-file=- --preload --timeout 60 --max-requests 50 --workers 1
bot: python bot_worker.py
