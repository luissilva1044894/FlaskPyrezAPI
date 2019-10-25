import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
	from decouple import config

	SQLALCHEMY_DATABASE_URI = config('DATABASE_URL') or 'sqlite:///{}.db'.format(__name__)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG = os.getenv('DEBUG', os.sys.platform == 'win32')
	ENV = 'dev' if DEBUG else 'production'
class DevelopementConfig(BaseConfig):
	DEBUG = True

class TestingConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///{}.db'.format(__name__))
