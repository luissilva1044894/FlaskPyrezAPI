#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import inspect
import re
import unicodedata

from boolify import boolify

from .environ import get_env

def decode(o, encoding='utf-8'):
  if hasattr(o, 'decode'):
    return o.decode(encoding=encoding or 'latin1')
  try:
    return str(o, encoding=encoding or 'latin-1')
  except (TypeError, ValueError):
    pass
  return o

def get_type(obj):
  """Handy wrapper for logging purposes"""
  return type(obj).__name__

def is_callable(func):
  """Determines objects that should be called before serialization"""
  #if is_callable(value): value = value()
  if callable(func):
    i = inspect.getfullargspec(func)
    if i.args == ['self'] and isinstance(func, MethodType) and not any([i.varargs, i.varkw]):
      return True
    return not any([i.args, i.varargs, i.varkw])
  return False

def is_hashable(obj):
  """Determine whether `obj` can be hashed."""
  try:
    hash(obj)#isinstance(obj, collections.Hashable)
  except TypeError:
    return False
  return True

def iterable(obj):
  try:
    return iter(obj)
  except Exception:
    pass
  return False

def on_heroku():
  return boolify(get_env('ON_HEROKU')) or 'heroku' in get_env('PYTHONHOME', '').lower()

def slugify(value):
  """Normalizes string, converts to lowercase, removes non-alpha characters, and converts spaces to hyphens.
  From: http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python"""
  return (re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '', unicodedata.normalize('NFKD', str(value)).encode('ascii', 'ignore').decode('utf-8', 'ignore'))) or value).strip().replace(' ', '-').replace("'", '').lower()
