#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import importlib
import os

from flask import Blueprint, g, request

from .exceptions import FieldRequired
from utils.web import get_value
'''
def decor1(f=None, **options):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      print('decor1')
      return f(*args, **kwargs)
    return wrapper
  if f:
    return decorator(f)
  return partial(decor1, options=options)
'''

def field_required(f=None, **options):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kw):
      _field, surpress_exceptions = options.get('field'), options.get('surpress_exceptions', False)
      if _field:
        try:
          _value = get_value(_field, request)
        except Exception:
          _value = None
        finally:
          if not _value and not surpress_exceptions:
            raise FieldRequired(_field[0] if isinstance(_field, (list, tuple)) else _field)
          setattr(g, _field[0] if isinstance(_field, (list, tuple)) else _field, _value)
      return f(*args, **kw)
    return wrapper
  if f:
    return decorator(f)
  return decorator

def auto_register_blueprints(f=None, **options):
  """Automagically register all blueprint packages."""
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      app = f(*args, **kwargs)
      __func__, _instance_of = getattr(app, options.get('call_method', 'register_blueprint')), options.get('instance_of', Blueprint)
      for _ in [ _ for _ in os.listdir('.') if not _[0] in ['_', '.']]:
        for path, subdirs, files in os.walk(_):
          for __ in [ _[:-3] for _ in files if not _[0] in ['_', '.'] and _[-3:]=='.py']:
            try:
              _name = os.path.join(path, __).replace('\\', '.').replace('/', '.')
              mod = importlib.import_module(_name)
            except (ModuleNotFoundError, ImportError, AttributeError) as exc:
              print(f'>>> Failed to load {_name.replace("app.", "")}: {exc}')
            else:
              for _ in mod.__dict__:
                _attr = getattr(mod, _)
                if (isinstance(_instance_of, str) and _instance_of in str(type(_attr))) or isinstance(_attr, _instance_of):
                  __func__(_attr)
                  print(f'>>> Loaded {_}: {_attr.name} ({mod.__name__})')# | {mod.__name__.split(".")[-2]}
      return app
    return wrapper
  if f:
    return decorator(f)
  return decorator
