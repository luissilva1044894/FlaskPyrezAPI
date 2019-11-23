#!/bin/bash

if [ -n "$CMD_LINE" ]; then
	$CMD_LINE
else
	echo "Running server as Gunicorn"
	gunicorn -b 0.0.0.0:$PORT wsgi:app --env FLASK_ENV=default --preload
fi
