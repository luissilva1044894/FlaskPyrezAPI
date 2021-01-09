
@echo off
echo.

cls
title Installing packages...

python -m pip install -r requirements.txt
PAUSE
GOTO end

:message
echo Something is not working
PAUSE

:end
echo Finished!
