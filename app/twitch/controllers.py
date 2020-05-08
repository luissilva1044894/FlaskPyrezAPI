#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import get_url
from ..utils.num import random_func

def random_viewer_function(_channel, _exclude, _ignore):
  _json = get_url(f'http://tmi.twitch.tv/group/user/{str(_channel).lower()}/chatters')
  for x in str(_ignore).split(','):
    if x.lower() == 'bots':
      _exclude += 'nightbot,priestbot,streamelements,streamlabs,botisimo,moobot'.split(',')
      _exclude += 'twitchprimereminder,commanderroot,anotherttvviewer,electricallongboard,lurxx'.split(',')
    elif x.lower() == 'mods':
      x = 'moderators'
    try:
      _json['chatters'].pop(x)
    except (KeyError, TypeError): #ValueError = _json['bots']
      pass
  _final_list = []
  if len(_json) < 1:
    return 'The list of users is empty'
  for x in _json['chatters']:
    for y in _json['chatters'][x]:
      for z in _exclude:
        if str(y).lower() == z.lower():
          try:
            _json['chatters'][x].remove(y)
          except (KeyError, TypeError):
            pass
    if len(_json['chatters'][x]) != 0:
      _final_list += _json['chatters'][x]
  if _final_list:
    return _final_list[random_func(0, len(_final_list) - 1)]
  return 'Error: No chatters'#https://community.nightdev.com/t/custom-api-random-viewer/17450/3

#!csgorank	Matchmaking: DMG Faceit: Level 10	everyone
#!csrank	MM: DMG Faceit: 10
#Tank: 5-0 4309 Support: 3-2 4363 Damage: 3-1-1 4430
#https://cai.tools.sap/blog/twitch-case-study-ai-bots/
#electric scateboard and commanderroot
#https://www.reddit.com/r/Twitch/comments/4qcsfq/an_updated_twitch_bot_list/
#Cole's current ranks: 2v2: Unranked (1438) | Solo 3v3: Unranked (1166) | 3v3: Champion III (1469) | Dropshot: Unranked (1133)
