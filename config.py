import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    from decouple import config, Csv
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PYREZ_AUTH_ID = config("PYREZ_AUTH_ID") or os.environ("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = config("PYREZ_DEV_ID") or os.environ("PYREZ_DEV_ID")
class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or "sqlite:///{}.db".format(__name__)
 
class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or "sqlite:///{}.db".format(__name__) 
 
class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///{}.db".format(__name__)
