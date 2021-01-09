#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.enums import Enum

class Platform(Enum):
  #PortalID
  Epic = 'epic'
  PC = 'pc'
  PS4 = 'ps4'
  PTS = 'pts'
  Steam = 'steam'
  Switch = 'switch'
  Xbox = 'xbox'

  def __int__(self):
    return {'steam': 5, 'ps4': 9, 'xbox': 10, 'switch': 22, 'epic': 28}.get(self.value, 1)

  def __str__(self):
    return {5: 'Steam', 9: 'PS4', 10: 'Xbox', 22: 'Nintendo Switch', 28: 'Epic Games'}.get(int(self), 'PC')

def get_platform(args):
  def fix_platform(v):
    return {'5': 'steam', '9': 'ps4', '10': 'xbox', '22': 'switch', '28': 'epic'}.get(str(v).lower(), 'pc')
  def get_plat(r):
    if hasattr(r, 'args'):
      r = r.args
    if hasattr(r, 'get'):
      for _ in ['platform', 'plat']:
        __ = r.get(_)
        if __:
          return fix_platform(__)
    return fix_platform(r)
  try:
    return Platform(get_plat(args))
  except (TypeError, ValueError):
    return Platform.PC
