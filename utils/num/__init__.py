#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

def format_decimal(data, form = ',d'):
  if data:
    return format(data, form)
  return 0

def hex_to_int(hex):
  if hex.startswith('#'):
    hex = hex[1:]
  return int(hex, 16)

def int_to_hex(num):
  return hex(num)[2:]

def rand(min_=0, max_=100, as_int=True, *, as_string=False, chars=None, size=32):
  if as_string:
    return ''.join(random.choice(chars or (string.ascii_letters + string.digits)) for x in range(size))
    #os.urandom(size)
  if as_int:
    return random.randint(min_, max_)
  return random.randrange(min_, max_)

def try_int(value, default=None):
  try:
    return int(value)
  except (TypeError, ValueError):
    return default or value

def winratio(wins, losses):
  matches_played = wins + losses
  if matches_played <= 0:
    matches_played = 1
  _w = (wins / matches_played) * 100.0
  if _w % 2 == 0:
    return int(_w)
  return round(_w, 2)
