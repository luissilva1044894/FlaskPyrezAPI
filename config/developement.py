
from .flask import Flask
class Developement(Flask):
	DEVELOPMENT, ENV = True, 'development'
	LOG_LEVEL = 'debug'
