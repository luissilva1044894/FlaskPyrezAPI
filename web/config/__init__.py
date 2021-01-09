#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask config class."""
import os
from datetime import timedelta

from boolify import boolify

from utils.environ import get_env
from utils.num import rand

base_dir = os.path.abspath(os.path.dirname(__file__))
_LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

class BaseConfig(object):
  """General Configuration."""
  TOP_LEVEL_DIR = os.path.abspath(os.curdir)

  SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI') or f'sqlite:///{os.path.join(TOP_LEVEL_DIR, "data/", "app.db")}'#'sqlite:///:memory:'
  #DATABASE_URI = config("DATABASE_URI", cast=URL)

  DEBUG = boolify(get_env('DEBUG'))

  SECRET_KEY = get_env('SECRET_KEY') or rand(as_string=True)

  PYREZ_AUTH_ID = get_env('PYREZ_AUTH_ID')
  PYREZ_DEV_ID = get_env('PYREZ_DEV_ID')

  #TESTING = config("TESTING", cast=bool, default=False)

  #LOG_LEVEL = config("APP_LOG_LEVEL", default="DEBUG")
  #LOG_MODE = config("LOG_MODE", default="local")

  #APP_PORT = config("APP_PORT", cast=int, default=5000)
  #APP_HOST = config("APP_HOST", cast=str, default="0.0.0.0")

  #DIST_ROOT = config("APP_DIST_ROOT", cast=str, default="dist/")
  #TEMPLATE_ROOT = config("APP_TEMPLATE_ROOT", cast=str, default=_LOCAL_DIR)

class Config(BaseConfig):
  PORT, HOST = get_env('PORT', 5000), get_env('HOST', '0.0.0.0')

  SQLALCHEMY_ECHO = False
  # Database URI
  SQLALCHEMY_TRACK_MODIFICATIONS = get_env('SQLALCHEMY_TRACK_MODIFICATIONS', False)

  CSRF_ENABLED = True

  #app.permanent_session_lifetime = datetime.timedelta(days=365) # you can also do this
  PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

  @staticmethod
  def init_app(app, env='APP_LOG_LEVEL'):
    import logging

    for handler in logging.getLogger(app.name).handlers[:]:
      handler.setLevel(app.config[env])

import typing

from .developement import Developement
from .testing import Testing
from .production import Production
from .discord import Discord

def _suppress_warnings():
  # warnings.filterwarnings("ignore", category=SomeWarning)
  pass


def get_config(app_env: typing.Optional[str]=None) -> Production:
  return {
    'development': Developement,
    'dev': Developement,
    'testing': Testing,
    'discord': Discord,
    'bot': Discord,
  }.get(str(app_env or '').lower(), Production)

def init_app(app, app_config: Config=None):
  _suppress_warnings()

  if app_config is None:
    app_config = get_config(app.env)
  app.config.from_object(app_config)
  # if not structlog.is_configured():
  #   from property_app.logging import initialize_logging
  #   initialize_logging()

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
