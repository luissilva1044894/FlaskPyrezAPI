#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import glob
import json
from json.decoder import JSONDecodeError

def get_sys_exec_root_or_drive():
  path = sys.executable
  while os.path.split(path)[1]:
    path = os.path.split(path)[0]
  return path

def open_if_exists(filename, mode='rb', encoding='utf-8'):
  """Returns a file descriptor for the filename if that file exists, otherwise ``None``."""
  if not os.path.isfile(filename) and (mode.rfind('r') != -1 or mode.rfind('a') != -1):
    return None
  try:
    import codecs
  except ImportError:
    try:
      f = open(filename, mode=mode, encoding=encoding)
    except ValueError:
      f = open(filename, mode=mode)
  else:
    f = codecs.open(filename, mode)
  finally:
    return f

def read_file(filename, *, mode='rb', encoding='utf-8', is_json=False):
  """Loads a file"""
  f, is_json = open_if_exists(filename, mode, encoding), 'json' in filename or is_json
  if f:
    if is_json:
      try:
        with f:
          return json.load(f)
      except json.decoder.JSONDecodeError:
        pass
      return {}
    if f.readable():
      return f.read()
    return f
