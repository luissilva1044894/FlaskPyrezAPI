#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

def try_int(value, default):
  try:
    return int(value)
  except ValueError:
    return default

def format_decimal(data, form = ',d'):
  if data:
    return format(data, form)
  return 0

def rand(min_=0, max_=100, as_int=True, *, as_string=False, chars=None, size=32):
  if as_string:
    return ''.join(random.choice(chars or (string.ascii_letters + string.digits)) for x in range(size))
  if as_int:
    return random.randint(min_, max_)
  return random.randrange(min_, max_)

def winratio(wins, losses):
  matches_played = wins + losses
  if matches_played <= 0:
    matches_played = 1
  _w = (wins / matches_played) * 100.0
  if _w % 2 == 0:
    return int(_w)
  return round(_w, 2)
