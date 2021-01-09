#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyrez

from . import (
  get_player_id,
  get_player_name,
  PLAYER_RANK_STRINGS,
)
from ..num import format_decimal

#from utils import get_champ_names, fix_champ_name
#from utils.web import get_lang_id

def get_lang_id(lang):
  return 1
def fix_champ_name(champ):
  return champ.lower().replace(' ', '').replace("'", '').replace('-', '')
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
  {**{slugify(_avatars[_]):num_or_string(_) for _ in _avatars}, **{str(num_or_string(_)):num_or_string(_) for _ in _avatars}}.get(str(_avatar_id), '0')

def decks_func(player, champ, platform, lang, api):
  return 'decks ...'
  player_id = get_player_id(api, player, platform)

def func(champ_name, player_id, _api, lang=1, nodeck_exc=Exception, nochamp_exc=Exception):
  champ_name, __champs__ = fix_champ_name(champ_name), get_champ_names()
  if not champ_name in __champs__:
    raise nochamp_exc
  p_loadouts = _api.getPlayerLoadouts(player_id, get_lang_id(int(lang)))
  if len(p_loadouts) <= 1:
    raise nodeck_exc
  cds = ''
  loadouts = [p_loadout for p_loadout in p_loadouts if fix_champ_name(p_loadout.godName) == champ_name]
  for loadout in loadouts:
    cardStr = '{}{}: {}'.format(' ' if len(cds) == 0 else ' · ', loadout.deckName, [f'{card.itemName} {card.points}' for card in loadout.cards]).replace("'", "")
    if len(cds + cardStr) <= 400: cds += cardStr
  if cds != '':
    return cds
  raise nodeck_exc

