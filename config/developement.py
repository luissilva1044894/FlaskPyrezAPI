
from .flask import Flask
class Developement(Flask):
	DEVELOPMENT, ENV = True, 'development'#dev
	LOG_LEVEL = 'debug'
