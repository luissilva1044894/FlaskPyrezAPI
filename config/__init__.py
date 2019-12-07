
"""Flask config class."""

class Config(object):
	"""General Configuration."""
	from utils import random_string, get_env, on_heroku
	from boolify import boolify
	import os

	BASE_DIR = os.path.abspath(os.path.dirname(__file__))
	TOP_LEVEL_DIR = os.path.abspath(os.curdir)

	ON_HEROKU = on_heroku()

	PYREZ_DEV_ID, PYREZ_AUTH_ID = get_env('PYREZ_DEV_ID', -1), get_env('PYREZ_AUTH_ID', None)

	DEV_SERVER = get_env('DEV_DISCORD_SERVER', 'https://discord.gg/XkydRPS')
	GITHUB_REPO = get_env('GITHUB_REPO', 'https://github.com/luissilva1044894/FlaskPyrezAPI')

	# SQLAlchemy
	SQLALCHEMY_DATABASE_URI = DATABASE_URI = get_env('DATABASE_URL') or 'sqlite:///{}'.format(get_env('DATABASE_FILE') or os.path.join(BASE_DIR, f'{__name__}.db'))#'sqlite:///:memory:'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	#SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	_binds = get_env('SQLALCHEMY_BINDS', default=None)
	SQLALCHEMY_BINDS = {}
	SQLALCHEMY_BINDS.update({'database': SQLALCHEMY_DATABASE_URI})
	if ON_HEROKU:
		for _ in os.environ:
			if _.upper().endswith('_URL'):#if 'DB_URL' in _.upper(): | _.upper().rfind('DB') != -1 and
				SQLALCHEMY_BINDS.update({_.split('_', 1)[0].lower() : get_env(_)})
		print(SQLALCHEMY_BINDS)
	if _binds:
		#https://docs.sqlalchemy.org/en/13/core/exceptions.html
		#https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/
		#https://flask-migrate.readthedocs.io/en/latest/
		for _ in _binds.split(','):
			__ = _.split(':', 1)
			SQLALCHEMY_BINDS.update({__[0].lower() : __[1] if __[1].rfind('://') != -1 else get_env(__[1])})
	# SECURITY WARNING: don't run with debug turned on in production!
	#Default: True if ENV is 'development', or False otherwise.
	DEBUG = boolify(get_env('DEBUG', default=not ON_HEROKU and os.sys.platform == 'win32' or os.name == 'nt'))

	# SECURITY WARNING: keep the secret key used in production secret!
	SECRET_KEY = get_env('SECRET_KEY', default=random_string(size=65))

	DEVELOPMENT = TESTING = not ON_HEROKU

from .developement import Developement
from .discord import Discord
from .testing import Testing
from .production import Production
