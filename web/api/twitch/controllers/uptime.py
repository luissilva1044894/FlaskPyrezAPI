#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.http import get_url

from datetime import datetime
from isodate import parse_datetime
import pytz

def get_uptime(start):
  """See how long the stream has been live for (must be live to get a time)."""
  delta = datetime.now(pytz.utc) - parse_datetime(start)
  hours, remainder = divmod(int(delta.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  years, days = divmod(days, 365)
  return f'{years}y, {days}d' if years else f'{days}d, {hours}h:{minutes}m' if days else f'{hours}h, {minutes}m' if hours else f'{minutes}m, {seconds}s'

  #fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
  #return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)

def uptime_func(channel, base_url, client_id, oauth_token, online_msg=None, offline_msg=None):
  def fix_base_url(url):
    if url[-1]=='/':
      return url
    return f'{url}/'
  data = get_url(f'{fix_base_url(base_url)}streams',
    headers={'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': client_id, 'Authorization': f'Bearer {oauth_token}'},
    params={'user_login': channel}, raise_for_status=False)
  if not data:
    #1 day, 6 hours, 33 minutes, 21 seconds
    return get_url(f'https://beta.decapi.me/twitch/uptime/{channel}?offline_msg={offline_msg}', surpress_exception=False)
  if 'data' in data:
    data = data['data']
    if data and isinstance(data, (tuple, list)) and len(data) > 0:
      data = data[0]
  if len(data) == 0:
    if offline_msg:
      return offline_msg
    return f'{channel} is currently offline'
  if 'error' in data:
    if 'message' in data:
      return data['message']
    return data['error']
  if 'type' in data and data['type'] == 'live':
    return f"{online_msg or ''} {get_uptime(data['started_at'])}"
  return data
