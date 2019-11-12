import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	from decouple import config
	from app.utils import random

	SQLALCHEMY_DATABASE_URI = config('DATABASE_URL') or os.getenv('DATABASE_URL', 'sqlite:///{}.db'.format('app' or __name__))
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# SECURITY WARNING: don't run with debug turned on in production!
	DEBUG = config('DEBUG') or os.getenv('DEBUG', os.sys.platform == 'win32')
	ENV = 'dev' if DEBUG else 'production'

	# SECURITY WARNING: keep the secret key used in production secret!
	SECRET_KEY = config('SECRET_KEY') or os.getenv('SECRET_KEY', random(as_string=True, size=50))
class DevelopementConfig(BaseConfig):
	DEVELOPMENT = DEBUG = True

class TestingConfig(BaseConfig):
	TESTING = DEVELOPMENT = DEBUG = True

class ProductionConfig(BaseConfig):
	TESTING = DEVELOPMENT = DEBUG = False
