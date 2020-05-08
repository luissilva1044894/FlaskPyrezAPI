#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from enum import Enum
from json.decoder import JSONDecodeError
import os

from flask import (
  escape,
  g,
  url_for,
)
import requests

from app.utils.file import read_json

class BaseEnumeration(Enum):
  def __str__(self):
    return str(self.value).lower()
  def __repr__(self):
    return self.__str__()
  def get_name(self):
    return str(self.name)
  def get_id(self):
    _ = str(self.value)
    if _.isnumeric():
      return int(_)
    return _
  def __hash__(self):
    return hash(str(self.value).lower())
  def __int__(self):
    try:
      return int(self.get_id())
    except ValueError:
      pass
    return -1
  def upper(self):
    return str(self).upper()
  def lower(self):
    return str(self).lower()

class PlatformsSupported(BaseEnumeration):
  PC = 'pc'
  PTS = 'pts'
  Xbox = '10'
  PS4 = '9'
  Switch = '22'
  Epic = '28'
def print_exception(exc):
  print(' : '.join([str(_) for _ in [type(exc), exc.args, exc]]))

def get_last_seen(last_seen, language=None):
  delta = datetime.utcnow() - last_seen
  hours, remainder = divmod(int(delta.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  years, days = divmod(days, 365)
  fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
  return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)

def replace(_input, _old, _new='', _split='', replace_or_split=False, _index=1):
  if replace_or_split:
    return _input.split(_split)[_index] or _input.replace(_old, _new)
  return _input.replace(_old, _new)

def get_url(url, as_json=True):
  _request = requests.get(url)
  if 'application/json' in _request.headers.get('Content-Type', '') or as_json:
    try:
      return _request.json()
    except (JSONDecodeError, ValueError):
      pass
  return _request.text
def get_query(request_args, key, default_value=None, default_key=None):
  if request_args:
    if hasattr(request_args, 'args'):
      request_args = request_args.args
    _x = request_args.get(key, default_key or None)
    if not _x:
      return default_value
    return _x
def getPlayerName(request_args):
  qry = request_args.get('query', default=None)
  if qry:
    playerName = qry[1:qry.rfind('"')] if qry.rfind('"') > 1 else qry.split(' ')[0]
  else:
    playerName = request_args.get('player', default=None)#str(request_args.get('query', default=str(request_args.get('player', default=None)).lower()).split(' ')[0]).lower()
  return None if not playerName or len(playerName) < 4 or (playerName.lower() in ['none', '0', 'null', '$(1)', 'query=$(querystring)', '[invalid%20variable]', 'your_ign', '$target']) else escape(playerName)

def getPlatform(request_args):
  qry = request_args.get('query', default=None)
  if qry:
    aux = qry[qry.rfind('"')+1:].split(' ') if qry.rfind('"') > 1 else qry.split(' ')
    if isinstance(aux, (type(()), type([]))) and len(aux) > 1:
      aux = aux[len(aux) - 1]
    else:
      aux = str(request_args.get('platform', default=None)).lower()
  else:
    aux = str(request_args.get('platform', default=None)).lower()
  if aux.startswith('xb'):
    return PlatformsSupported.Xbox
  if aux.startswith('switch'):
    return PlatformsSupported.Switch
  if aux.startswith('ps'):
    return PlatformsSupported.PS4
  if aux.startswith('pts'):
    return PlatformsSupported.PTS
  if aux.startswith('ep'):
    return PlatformsSupported.Epic
  return PlatformsSupported.PC

#def get_json(filename='langs'):
#  if '_json' not in g:
#    g._json = read_json(filename + '.json')
#  return g._json
def get_json(lang='en', *, key=None, force=False, folder='lang/'):
  if force or '_json' not in g:
    g._json = read_json(f'{folder}{lang}.json')
  if key:
    return g._json[key]
  return g._json
def fix_url_for(_json, blueprint_name):
  for _ in range(len(_json['HTML']['CMD_TABLE'][blueprint_name.upper()])):
    for __ in range(len(_json['HTML']['CMD_TABLE'][blueprint_name.upper()][_])):
      #input(_json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__])
      if _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__]:
        if _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__].startswith('url_for'):
          _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__] = url_for('{}.{}'.format(blueprint_name, _json['HTML']['CMD_TABLE'][blueprint_name.upper()][_][__].split(':')[1]), _external=True)
  return _json

def get_env(name, default=None, verbose=False):
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

def to_bool(value=None):
  """
  https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python

  >>> import json
  >>> json.loads("false".lower())
  False
  >>> json.loads("True".lower())
  True
  """
  if isinstance(value, bool):
      return value
  return { #if lower_value in valid: return valid[lower_value]
    '1': True, 'true': True, 't': True, 'on': True, 'yes': True,
    '0': False, 'false': False, 'f': False, 'off': False, 'no': False,
  }.get(str(value).lower(), False)#if not isinstance(value, basestring):
