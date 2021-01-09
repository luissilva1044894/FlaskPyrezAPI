#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from utils.http import get_html
from utils.num import winratio

def get_battle_net(battle_net):
  return battle_net.replace('#', '-', 1)

def get_rank_name(skill_rating):
  if skill_rating >= 1 and skill_rating <= 1499:
  	return 'Bronze'
  if skill_rating >= 1500 and skill_rating <= 1999:
  	return 'Silver'
  if skill_rating >= 2000 and skill_rating <= 2499:
  	return 'Gold'
  if skill_rating >= 2500 and skill_rating <= 2999:
  	return 'Platinum'
  if skill_rating >= 3000 and skill_rating <= 3499:
  	return 'Diamond'
  if skill_rating >= 3500 and skill_rating <= 3999:
  	return 'Master'
  if skill_rating >= 4000:
    return 'Grandmaster'
  return '???'

def rank_func(battle_net, platform, lang=None, *, paladins_like=False, format_average_sr=False):
  if not battle_net:
    return '🚫 ERROR: Player not specified!'
  try:
    #https://github.com/Addonexus/OverwatchWebscraper/blob/master/scraper.py
    rank = {}
    last_time = time.time()
    r = get_html(f'https://playoverwatch.com/en-us/career/{str(platform).lower()}/{get_battle_net(battle_net)}')
    for item in (r.findAll('div', {'class': 'competitive-rank-role'}) if hasattr(r, 'findAll') else []):
      rank[str(item.findAll('div', {'class': 'competitive-rank-tier-tooltip'})[0]['data-ow-tooltip-text'].split()[0]).lower()] = int(item.findAll('div', {'class': 'competitive-rank-level'})[0].text)
    print(f'That took {time.time() - last_time} seconds\r\n\r\n{rank}')
  except:
    pass
  else:
    try:
      _ratings, high_sr, __x__, __y__ = [], -1, 0, 0
      for x in rank:
        if format_average_sr:
          __x__ += 1
          __y__ += rank[x]
        if rank[x] > high_sr:
          high_sr = rank[x]
        _ratings.append(f'{x.title()} {rank[x]} SR')
      _rat = ' | '.join(_ratings)
      _rank = __x__ / __y__ if format_average_sr else high_sr
    except:
      pass
    else:
      if rank:
        return f'{battle_net.split("-")[0]} is {get_rank_name(_rank)} ({_rank} SR){f" - {_rat}" if _rat else ""}'
  _json = get_html(f'https://ow-api.com/v1/stats/{platform}/us/{get_battle_net(battle_net)}/profile', surpress_exception=False)
  if _json and isinstance(_json, dict):
    if _json.get('error'):
      return '🚫 ERROR: ' + _json['error']
    if _json.get('private'):
      return '🔒 ERROR: Private account!'
    _ratings, high_sr = [], -1
    for x in _json.get('ratings', ()):
      if x['level'] > high_sr:
        high_sr = x['level']
      _ratings.append('{} {} SR'.format(x['role'].title(), x['level']))
    _rat = ' | '.join(_ratings)
    _rank = _json['rating'] if format_average_sr else high_sr
    if paladins_like:
      return "{} is {} ({} SR{}) with {} wins and {} losses. (Win rate: {}%)".format(_json['name'].split('#')[0], get_rank_name(_rank), _rank, ' - {}'.format(_rat) if _rat else '', _json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played'] - _json['competitiveStats']['games']['won'], winratio(_json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played']))
    return f'{_json["name"].split("#")[0]} is {get_rank_name(_rank)} ({_rank} SR){f" - {_rat}" if _rat else ""}'
  return '🚫 ERROR'
