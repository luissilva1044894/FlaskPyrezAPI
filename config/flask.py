
from . import Config
class Flask(Config):
	"""Set Flask configuration vars."""
	"""Base configuration."""
	#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dev.sqlite')
	from utils import random_string, get_env
	from boolify import boolify
	import os

	PORT, HOST = get_env('PORT', default=5000), get_env('HOST', default='0.0.0.0')

	LOG_PATH, LOG_FILENAME, LOG_LEVEL = get_env('LOG_PATH', 'logs'), get_env('LOG_FILENAME', 'flask.log'), get_env('LOG_LEVEL', 'info')

	SQLALCHEMY_ECHO = False

	#app.permanent_session_lifetime = datetime.timedelta(days=365) # you can also do this
	from datetime import timedelta
	PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
