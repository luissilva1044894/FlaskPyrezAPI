#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boolify import boolify
import pyrez

#https://github.com/arslee07/OpenMod/blob/master/src/data/locales.json
#https://github.com/EasyThe/ThothBotCore/blob/master/ThothBotCore/Connections/StatusPage.cs
#https://github.com/EasyThe/ThothBotCore/blob/master/ThothBotCore/Utilities/StatusTimer.cs
#https://stk4xr7r1y0r.statuspage.io/api/v2/summary.json
#https://github.com/GoByeBye/DiscoRape

_invalid_input_ = ['none', '0', 'null', '$(1)', 'query=$(querystring)', '$(querystring)', '[invalid%20variable]', 'your_ign', '$target']

PLAYER_RANK_STRINGS = {
  'en' : {
    0: 'Unranked',
    1: 'Bronze 5', 2: 'Bronze 4', 3: 'Bronze 3', 4: 'Bronze 2', 5: 'Bronze 1',
    6: 'Silver 5', 7: 'Silver 4', 8: 'Silver 3', 9: 'Silver 2', 10: 'Silver 1',
    11: 'Gold 5', 12: 'Gold 4', 13: 'Gold 3', 14: 'Gold 2', 15: 'Gold 1',
    16: 'Platinum 5', 17: 'Platinum 4', 18: 'Platinum 3', 19: 'Platinum 2', 20: 'Platinum 1',
    21: 'Diamond 5', 22: 'Diamond 4', 23: 'Diamond 3', 24: 'Diamond 2', 25: 'Diamond 1',
    26: 'Master', 27: 'Grandmaster'
  },
  'es' : {
    0: 'Unranked',#Qualifying
    1: 'Bronce 5', 2: 'Bronce 4', 3: 'Bronce 3', 4: 'Bronce 2', 5: 'Bronce 1',
    6: 'Plata 5', 7: 'Plata 4', 8: 'Plata 3', 9: 'Plata 2', 10: 'Plata 1',
    11: 'Oro 5', 12: 'Oro 4', 13: 'Oro 3', 14: 'Oro 2', 15: 'Oro 1',
    16: 'Platino 5', 17: 'Platino 4', 18: 'Platino 3', 19: 'Platino 2', 20: 'Platino 1',
    21: 'Diamante 5', 22: 'Diamante 4', 23: 'Diamante 3', 24: 'Diamante 2', 25: 'Diamante 1',
    26: 'Maestro', 27: 'Gran maestro'
  },
  'pl' : {
    0: 'Brak rangi',
    1: 'Brąz 5', 2: 'Brąz 4', 3: 'Brąz 3', 4: 'Brąz 2', 5: 'Brąz 1',
    6: 'Srebro 5', 7: 'Srebro 4', 8: 'Srebro 3', 9: 'Srebro 2', 10: 'Srebro 1',
    11: 'Złoto 5', 12: 'Złoto 4', 13: 'Złoto 3', 14: 'Złoto 2', 15: 'Złoto 1',
    16: 'Platyna 5', 17: 'Platyna 4', 18: 'Platyna 3', 19: 'Platyna 2', 20: 'Platyna 1',
    21: 'Diament 5', 22: 'Diament 4', 23: 'Diament 3', 24: 'Diament 2', 25: 'Diament 1',
    26: 'Mistrz', 27: 'Arcymistrz'
  },
  'pt' : {
    0: 'Unranked',
    1: 'Bronze 5', 2: 'Bronze 4', 3: 'Bronze 3', 4: 'Bronze 2', 5: 'Bronze 1',
    6: 'Prata 5', 7: 'Prata 4', 8: 'Prata 3', 9: 'Prata 2', 10: 'Prata 1',
    11: 'Ouro 5', 12: 'Ouro 4', 13: 'Ouro 3', 14: 'Ouro 2', 15: 'Ouro 1',
    16: 'Platina 5', 17: 'Platina 4', 18: 'Platina 3', 19: 'Platina 2', 20: 'Platina 1',
    21: 'Diamante 5', 22: 'Diamante 4', 23: 'Diamante 3', 24: 'Diamante 2', 25: 'Diamante 1',
    26: 'Mestre', 27: 'Grão-mestre'
  },
}

def get_rank_name(tier):
  if tier >= 1 and tier <= 5:
    return 'Bronze'
  if tier >= 6 and tier <= 10:
    return 'Silver'
  if tier >= 11 and tier <= 15:
    return 'Gold'
  if tier >= 16 and tier <= 20:
    return 'Platinum'
  if tier >= 21 and tier <= 25:
    return 'Diamond'
  if tier == 26:
    return 'Master'
  if tier == 27:
    return 'Grandmaster'
  if tier == 0:
    return 'Unranked'
  return '???'

def get_player_name(player):
  try:
    return (player.hzPlayerName or player.hzGamerTag) or player.playerName
  except Exception:
    pass
  return player.playerName

def get_player_id(api, player, platform=None):
  if not player or player in _invalid_input_:
    return 0#<null
  player = player.strip().lower()
  if str(player).isnumeric():
    if len(str(player)) > 5 or len(str(player)) < 12:
      return player
  temp = api.getPlayerId(player, platform) if platform and str(platform).isnumeric() else api.getPlayerId(player)
  if not temp or isinstance(temp, (list, tuple)) and boolify(temp[0]['privacy_flag']):
    raise pyrez.exceptions.PrivatePlayer(player)#-1 == <not found
  return getattr(temp[0], 'playerId' if hasattr(temp[0], 'playerId') else 'player_id')

'''
from utils.enums import Enum

class Platform(Enum):
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
'''
