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
