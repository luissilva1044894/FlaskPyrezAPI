
from .flask import Flask
class Testing(Flask):#Staging
	TESTING = DEVELOPMENT = DEBUG = True
	LOG_LEVEL = 'info'
