import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    from decouple import config, Csv
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PYREZ_AUTH_ID = os.environ("PYREZ_AUTH_ID") or config("PYREZ_AUTH_ID")
    PYREZ_DEV_ID = os.environ("PYREZ_DEV_ID") or config("PYREZ_DEV_ID")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///{}.db".format(__name__)
class DevelopementConfig(BaseConfig):
    DEBUG = True
 
class TestingConfig(BaseConfig):
    DEBUG = True
 
class ProductionConfig(BaseConfig):
    DEBUG = False
