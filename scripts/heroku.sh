#!/bin/bash

if [ "$ASYNC" ]; then
    hypercorn -b 0.0.0.0:${PORT} asgi:app
else
    gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
fi
