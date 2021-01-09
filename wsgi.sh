
#!/usr/bin/env bash

#export ENVIRONMENT=dev

pkill -9 -f main.py
/usr/bin/python3 main.py || (echo "Error" && exit)
echo "Done"
