#!/bin/bash

if [ "$ASYNC" ]; then
    if [ "$UVICORN" ]; then
    	gunicorn asgi:app -w 4 -k uvicorn.workers.UvicornWorker
    else
    	hypercorn -b 0.0.0.0:${PORT} asgi:app
    fi
else
    gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
fi
