#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import getenv
try:
  from dotenv import load_dotenv
except ImportError:
  try:
    from decouple import config as getenv, Csv, UndefinedValueError
  except ImportError:
    pass
else:
  if os.path.isfile('.env'):
    load_dotenv('.env', override=True)#verbose=False
finally:
  def get_env(name, _default=None, *, cast=None):
    if cast:
      return getenv(name, cast=Csv())
    return getenv(name) or _default

from ..__init__ import on_heroku

def update_env(env={}, app_name=None):
  """https://github.com/TomoTom0/DiscordBot_Heroku_Stat.ink/blob/main/src/basic.py"""
  if on_heroku():
    for k, v in env.items():
      os.environ[k] = v
    app_name = app_name or get_env('HEROKU_APP_NAME')
    if app_name:
      return requests.patch(f'https://api.heroku.com/apps/{app_name}/config-vars',
        headers={'Authorization':f"Bearer {get_env('HEROKU_API_KEY')}",'Content-Type':'application/json','Accept':'application/vnd.heroku+json; version=3'},
        json=env,
      )
