#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.http import get_url

def get_channel_emotes(channel_id):
  _j = get_url(f'https://api.twitchemotes.com/api/v4/channels/{channel_id}')
  if not isinstance(_j, dict):
    return ''
  return ' '.join([e.get('code', '') for e in _j.get('emotes', []) if e.get('code')])
