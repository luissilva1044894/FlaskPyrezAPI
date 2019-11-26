#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
class BaseEnumeration(Enum):
    def __str__(self):
        return str(self.value).lower()
    def __hash__(self):
        return hash(str(self.value).lower())
class LanguagesSupported(BaseEnumeration):
    English = 'en'
    Portuguese = 'pt'
    Spanish = 'es'
    Polish = 'pl'
class PlatformsSupported(BaseEnumeration):
    PC = 'pc'
    PTS = 'pts'
    Xbox = '10'
    PS4 = '9'
    Switch = '22'
def print_exception(exc):
    print(' : '.join([str(_) for _ in [type(exc), exc.args, exc]]))

def root_path():
    import os
    return os.path.dirname(os.path.abspath(__file__)).replace(__name__, '')

def replace(_input, _old, _new='', _split='', replace_or_split=False, _index=1):
    if replace_or_split:
        return _input.split(_split)[_index] or _input.replace(_old, _new)
    return _input.replace(_old, _new)

def random(min=0, max=100, *, as_int=True, args=None):
    import random
    if args:
        return random.choice(args)#if isinstance(args, list) and len(args) > 0:
    if as_int:
        return random.randint(min, max)
    return random.randrange(min, max)

def random_string(chars=None, size=32):
    from random import choice
    if not chars:
        import string
        chars = string.ascii_letters + string.digits # + string.punctuation
    return ''.join(choice(chars) for _ in range(size))

def load_locate_json(lang, folder='lang'):
    from utils.file import read_file, join_path
    return read_file(join_path(['data', folder, '{}.json'.format(lang)]), is_json=True)

def get_url(url, as_json=True):
    import requests
    for _ in range(5):
        try:
            _request = requests.get(url)
            if as_json:
                from json.decoder import JSONDecodeError
                try:
                    return _request.json()
                except (JSONDecodeError, ValueError):
                    pass
            return _request.text
        except requests.exceptions.ConnectionError:
            import time
            time.sleep(1)
    return None
def get_env(name, default=None, verbose=False):
    import os
    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
        #try:
        #    return os.environ[name] or default
        #except KeyError:
        #    return default
    else:
        #from pathlib import Path  # python3 only
        load_dotenv(verbose=verbose)#,dotenv_path=Path('.') / '.env'
    finally:
        return os.getenv(name) or default

def get_timestamp(_format='%Y-%m-%d %H:%M:%S'):
    from datetime import datetime
    return datetime.now().strftime(_format)

def format_timestamp(timestamp, _format='MMMM D, YYYY'):
  try:
    import arrow
    try:
      _timestamp = arrow.get(timestamp, _format)
    except (arrow.parser.ParserMatchError, arrow.parser.ParserError):
      pass
    else:
      return _timestamp.isoformat()#_timestamp.format('DD-MMM-YYYY HH:mm:SS ZZ')
      # 2019-11-12T23:31Z | 2019-11-18T18:36:32+00:00
  except importError:
    pass

def last_seen(locale, date):
    try:
        import arrow
    except ImportError:
        from datetime import datetime
        delta = datetime.utcnow() - date
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
        return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)
    else:
        c = arrow.utcnow() - date
        if c.days:
            return arrow.utcnow().shift(days=-c.days, seconds=c.seconds, microseconds=c.microseconds).humanize(locale=locale)
        if c.seconds:
            return arrow.utcnow().shift(seconds=-c.seconds).humanize(locale=locale)
        return arrow.utcnow().shift(microseconds=c.microseconds).humanize(locale=locale)
def fix_champ_name(champ):
    return champ.lower().replace(' ', '').replace("'", '').replace("-", '')
def get_champ_names(lang=None):
  '''
  __champs__, __trans_champ__ = {}, {}
  for i in [1, 2, 3, 5, 7, 9, 10, 11, 12, 13]:
    __trans_champ__[i] = {}
    for champ in get_url(f'https://cms.paladins.com/wp-json/api/champion-hub/{i}'):
      if champ and not fix_champ_name(fix_champ_name(champ.get('name'))) in __champs__:
        __champs__[fix_champ_name(champ.get('name'))] = fix_champ_name(champ.get('feName'))
      __trans_champ__[i][fix_champ_name(champ.get('feName'))] = fix_champ_name(champ.get('name'))
  if translated:
    return __trans_champ__
  return __champs__
  '''
  return [fix_champ_name(_.get('name')) for _ in get_url(f'https://cms.paladins.com/wp-json/api/champion-hub/{lang or 1}')]
"""
https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python

>>> import json
>>> json.loads("false".lower())
False
>>> json.loads("True".lower())
True
"""

def get_root_path(import_name):
  import sys
  import pkgutil
  import os
  mod = sys.modules.get(import_name)
  if mod is not None and hasattr(mod, '__file__'):
    return os.path.dirname(os.path.abspath(mod.__file__))
  loader = pkgutil.get_loader(import_name)
  if loader is None or import_name == '__main__':
    return os.getcwd()
  if hasattr(loader, 'get_filename'):
    filepath = loader.get_filename(import_name)
  else:
    __import__(import_name)
    mod = sys.modules[import_name]
    filepath = getattr(mod, '__file__', None)
    if not filepath:
      raise RuntimeError(f'No root path can be found for the provided module "{import_name}"')
  # filepath is import_name.py for a module, or __init__.py for a package.
  return os.path.dirname(os.path.abspath(filepath))
