#!/bin/bash

#if [ -n "$CMD_LINE" ]; then
	#$CMD_LINE
if [ -n "$ASYNC" ]; then
	echo "Running (async) server as Hypercorn"
	hypercorn -b 0.0.0.0:${PORT} asgi:app
else
	echo "Running server as Gunicorn"
	gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
fi
