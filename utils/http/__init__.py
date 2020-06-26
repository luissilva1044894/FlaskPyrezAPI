#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup

def get_url(url, as_json=True, raise_for_status=True, surpress_exception=True):
  try:
    _r = requests.get(url)
  except Exception:
    if not surpress_exception:
      raise
    return None
  if raise_for_status:
    _r.raise_for_status()
  if 'application/json' in _r.headers.get('Content-Type', '') or as_json:
    try:
      return _r.json()
    except (JSONDecodeError, ValueError, AttributeError):
      pass
  return _r.text if hasattr(_r, 'text') else _r

def get_html(markup, builder='html.parser', *, raise_for_status=True, surpress_exception=True):
  if str(markup).startswith('http'):
    markup = get_url(markup, raise_for_status=raise_for_status, surpress_exception=surpress_exception)
  try:
    return BeautifulSoup(markup, builder)
  except (TypeError, ValueError):
    pass
