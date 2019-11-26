
from .flask import Flask
class Production(Flask):
	TESTING = DEVELOPMENT = DEBUG = False
	ENV = 'production'
	LOG_LEVEL = 'error'
