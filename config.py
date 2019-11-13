import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	from app.utils import random, get_env, to_bool

	SQLALCHEMY_DATABASE_URI = get_env('DATABASE_URL', default='sqlite:///{}.db'.format('app' or __name__))#'sqlite:///:memory:'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	_binds = get_env('SQLALCHEMY_BINDS', default=None)
	if _binds:
		#https://docs.sqlalchemy.org/en/13/core/exceptions.html
		#https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/
		#https://flask-migrate.readthedocs.io/en/latest/
		SQLALCHEMY_BINDS = {}
		for _ in _binds.split(','):
			__ = _.split(':', 1)
			SQLALCHEMY_BINDS.update({__[0].lower() : __[1] if __[1].rfind('://') != -1 else get_env(__[1])})
		print(SQLALCHEMY_BINDS)
	# SECURITY WARNING: don't run with debug turned on in production!
	#Default: True if ENV is 'development', or False otherwise.
	DEBUG = to_bool(get_env('DEBUG', default=os.sys.platform == 'win32' or os.name == 'nt'))

	# SECURITY WARNING: keep the secret key used in production secret!
	SECRET_KEY = get_env('SECRET_KEY', default=random(as_string=True, size=65))

	DEVELOPMENT = TESTING = False

	@property
	def DATABASE_URI(self):
		return SQLALCHEMY_DATABASE_URI
class DevelopementConfig(Config):
	DEVELOPMENT = True
	ENV = 'development'#dev

class TestingConfig(Config):#StagingConfig
	TESTING = DEVELOPMENT = DEBUG = True

class ProductionConfig(Config):
	TESTING = DEVELOPMENT = DEBUG = False
	ENV = 'production'
