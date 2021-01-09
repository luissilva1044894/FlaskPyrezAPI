#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import importlib
import os
import sys
import traceback

from flask import (
  Blueprint,
  g,
  render_template,
  request,
)

from .exceptions import FieldRequired
from . import get_value
from utils import decode
from utils.crypto import (
  decrypt,
  hashing,
  encrypt,
)
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
      _field, surpress_exceptions, call_method = options.get('field'), options.get('surpress_exceptions', False), options.get('call_method', None)
      if _field:
        try:
          _value = get_value(_field, request)
        except Exception:
          _value = None
        finally:
          if not _value and not surpress_exceptions:
            raise FieldRequired(_field[0] if isinstance(_field, (list, tuple)) else _field)
          if call_method and callable(call_method):
            _value = call_method(_value)
          setattr(g, _field[0] if isinstance(_field, (list, tuple)) else _field, _value)
      return f(*args, **kw)
    return wrapper
  if f:
    return decorator(f)
  return decorator

def require_key(f=None, **options):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kw):
      if '@' in g.key:
        key, hash_ = g.key.split('@')
        _msg = encrypt(hashing(g.channel, key), key)
        return f'{decode(hashing(g.channel, key))} \r\n\r\n{decode(_msg)} \r\n\r\n{decode(decrypt(_msg, key))} \r\n\r\n{decrypt(_msg, key) == hash_.encode()}'
      _msg = encrypt(hashing(g.channel, g.key), g.key)
      return f'{decode(_msg)} \r\n\r\n{decode(decrypt(_msg, g.key))}'
      return f(*args, **kw)
    return wrapper
  if f:
    return decorator(f)
  return decorator

#@decorators.templated('login.html')
def templated(template=None):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if template is None:
        template = request.endpoint.replace('.', '/') + '.html'
      ctx = f(*args, **kwargs)
      if not isinstance(ctx, dict):
        return ctx
      return render_template(template, **ctx or {})
    return decorated_function
  return decorator

def auto_register_blueprints(f=None, path_='web', **options):
  """Automagically register all blueprint packages."""
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      def _print(app, msg):
        if hasattr(app, 'logger'):
          return app.logger.info(msg)
        return print(msg)
      app = f(*args, **kwargs)
      __func__, _instance_of = getattr(app, options.get('call_method', 'register_blueprint')), options.get('instance_of', Blueprint)
      for _ in [ _ for _ in os.listdir('.') if not _[0] in ['_', '.'] and _ == path_]:
        for path, subdirs, files in os.walk(_):
          for __ in [ _[:-3] for _ in files if not _[0] in ['_', '.'] and _[-3:]=='.py']:
            try:
              _name = os.path.join(path, __).replace('\\', '.').replace('/', '.')
              mod = importlib.import_module(_name)
            except (ModuleNotFoundError, ImportError, AttributeError, NameError) as e:
              print(f'>>> Failed to load {_name}\n{type(e).__name__}: {e}')
              traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
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
