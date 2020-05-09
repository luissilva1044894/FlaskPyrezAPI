#!/usr/bin/env python
# -*- coding: utf-8 -*-

_invalid_input_ = ['none', '0', 'null', '$(1)', 'query=$(querystring)', '[invalid%20variable]', 'your_ign', '$target']

def get_player_id(api, player_name, platform=None):
  if not player_name or player_name in _invalid_input_:
    return 0
  player_name = player_name.strip().lower()
  if str(player_name).isnumeric():
    if len(str(player_name)) > 5 or len(str(player_name)) < 12:
      return player_name
  temp = api.getPlayerId(player_name, platform) if platform and str(platform).isnumeric() else api.getPlayerId(player_name)
  if not temp:
    return -1
  return getattr(temp[0], 'playerId' if hasattr(temp[0], 'playerId') else 'player_id')
