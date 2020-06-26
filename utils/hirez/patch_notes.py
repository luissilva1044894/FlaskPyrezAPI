#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..http import get_url

def get_links(name):
  def get_home_page(name):
    return {
      'paladins_strike': 'https://paladinsstrike.com',
      'realm_royale': 'https://realmroyale.com',
      'smite': 'https://smitegame.com',
      'smite_blitz': 'https://playsmiteblitz.com',
    }.get(str(name), 'https://paladins.com')

def get_patch_notes(website_api, website, lang=None, *, want_json=False):
  def get_posts(web, query, lng=None):
    return get_url(f'{web}get-posts/{lng or 1}?&search={query}')
  def fix_patch_notes(web, query, lng):
    resp = get_posts(web, query, lng)
    if resp and isinstance(resp, list) and isinstance(resp[0], dict):
      '''
      def _dict(_):
        _['url'] = f"{_['title']} · {web}news/{_['slug']}?lng={lng}"
        return _
      return [_dict(_) for _ in resp if 'title' in _ and 'slug' in _]
      '''
      return [{**_, **{'url': f"{_['title']} · {website}news/{_['slug']}?lng={lng}"}} for _ in resp if 'title' in _ and 'slug' in _]
      '''
      for _ in resp:
        if 'title' in _ and 'slug' in _:
          print(_)
          #_ is dict
          resp[_]['url'] = f"{resp[_]['title']} · {web}news/{resp[_]['slug']}?lng={lng}"
          #''.join([resp[_]['title'], ' · ', web, 'news/', resp[_]['slug'], '?lng=', lng])
      '''
    return resp
  _posts = get_posts(website_api, 'update%20notes')
  if _posts and isinstance(_posts, list) and len(_posts) > 0:
    _title = _posts[0]['title']
    _patchs = fix_patch_notes(website_api, _title[:_title.rfind('update') - 1], lang)
    if _patchs and isinstance(_patchs, list) and len(_patchs) > 0:
      if want_json:
        return _patchs
      return _patchs[-1]['url']
  return f'{website}news/?lng={lang}'
