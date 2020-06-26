
"""Flask config class."""
import os
from datetime import timedelta

from utils.environ import get_env
from utils.num import rand
from boolify import boolify
base_dir = os.path.abspath(os.path.dirname(__file__))
class BaseConfig(object):
  """General Configuration."""
  TOP_LEVEL_DIR = os.path.abspath(os.curdir)

  SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI') or f'sqlite:///{os.path.join(TOP_LEVEL_DIR, "app.db")}'#'sqlite:///:memory:'
  DEBUG = boolify(get_env('DEBUG')) or False

  SECRET_KEY = get_env('SECRET_KEY') or rand(as_string=True)

class Config(BaseConfig):
  PORT, HOST = get_env('PORT', 5000), get_env('HOST', '0.0.0.0')

  SQLALCHEMY_ECHO = False
  # Database URI
  SQLALCHEMY_TRACK_MODIFICATIONS = get_env('SQLALCHEMY_TRACK_MODIFICATIONS', False)

  CSRF_ENABLED = True

  #app.permanent_session_lifetime = datetime.timedelta(days=365) # you can also do this
  PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

from .developement import Developement
from .testing import Testing
from .production import Production
from .discord import Discord

def get_config(name=None):
  return {
    'development': Developement,
    'dev': Developement,
    'testing': Testing,
    'discord': Discord,
    'bot': Discord,
  }.get(str(name or '').lower(), Production)

'''

class TestConfig(BaseConfig):
    APP_ENV = "test"
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_PROFILER_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class LocalhostConfig(BaseConfig):
    APP_ENV = "localhost"
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class StagingConfig(BaseConfig):
    APP_ENV = "staging"
    DEBUG = True
    TESTING = False
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProductionConfig(BaseConfig):
    APP_ENV = "production"
    TESTING = False


config = {
    '_baseconfig': "config.BaseConfig",
    'localhost': "config.LocalhostConfig",
    'test': "config.TestConfig",
    'staging': "configStagingConfig",
    'production': "configProductionConfig",
}

__all__ = ['config']
'''
