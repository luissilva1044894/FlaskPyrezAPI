#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from random import (
  choice,
  randint,
  randrange,
)
def try_int(value, default):
  try:
    return int(value)
  except (ValueError, TypeError):
    return default

def format_decimal(data, form = ',d'):
  if data:
    return format(data, form)
  return 0

def random_func(min=0, max=100, as_int=True, *, as_string=False, chars=None, size=32):
  if as_string:
    return ''.join(choice(chars or (string.ascii_letters + string.digits)) for x in range(size))
  if as_int:
    return randint(min, max)
  return randrange(min, max)

def winratio(wins, matches_played):
  _w = wins /((matches_played) if matches_played > 1 else 1) * 100.0
  if _w % 2 == 0:
    return int(_w)
  return round(_w, 2)
