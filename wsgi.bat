
@echo off
echo.

cls
title Lauching...
python wsgi.py
PAUSE
GOTO end

:message
echo Something is not working
PAUSE

:end
