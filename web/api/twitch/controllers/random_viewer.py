#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.http import get_url
from utils.num import rand

def random_viewer_func(channel, _exclude, _ignore):
  _json = get_url(f'http://tmi.twitch.tv/group/user/{str(channel).lower()}/chatters')
  if _json and isinstance(_json, dict) and _json.get('chatter_count', -1) > 0:
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
        for z in (_exclude or []):
          if str(y).lower() == z.lower():
            try:
              _json['chatters'][x].remove(y)
            except (KeyError, TypeError):
              pass
      if len(_json['chatters'][x]) != 0:
        _final_list += _json['chatters'][x]
    if _final_list:
      return _final_list[rand(0, len(_final_list) - 1)]
  return get_url(f'https://2g.be/twitch/randomviewer.php?channel={channel}', surpress_exception=False)#https://community.nightdev.com/t/custom-api-random-viewer/17450/3
