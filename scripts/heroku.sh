#!/bin/bash

if [ -n "$SERVER_MODE" ]; then
    if [ {"$SERVER_MODE"^^} == *"GUNICORN"* ]; then
    	echo "Running (async) server as Gunicorn"
    	gunicorn -b 0.0.0.0:$PORT asgi:app -w 4 -k uvicorn.workers.UvicornWorker
    elif [ {"$SERVER_MODE"^^} == *"UVICORN"* ]; then
    	echo "Running (async) server as Uvicorn"
    	uvicorn asgi:app --host 0.0.0.0 --port $PORT
    else
    	echo "Running (async) server as Hypercorn"
    	hypercorn -b 0.0.0.0:${PORT} asgi:app
    fi
else
    echo "Running (sync) server as Gunicorn"
    gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
fi
