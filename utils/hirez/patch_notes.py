#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..http import get_url
from ..environ import get_env
from web.utils import fix_blueprint_name
from ..num import try_int

def get_links(name):
  def get_home_page(name):
    return get_env(f'{name}_WEBSITE') or {
      'paladins_strike': 'https://paladinsstrike.com/',
      'realm_royale': 'https://realmroyale.com/',
      'rogue_company': 'https://roguecompany.com/',
      'smite': 'https://smitegame.com/',
      'smite_blitz': 'https://playsmiteblitz.com/',
    }.get(str(name), 'https://paladins.com/')
  def get_web_api(name):
    return get_env(f'{name}_WEBSITE_API')
  name = fix_blueprint_name(name)
  return get_home_page(name), get_web_api(name)

def get_patch_notes(blueprint, lang=None, *, requested_json=False, use_slug=False):
  #print(lang, str(lang), lang.lang_code, lang.supported)
  def get_posts(web, query, lng=None, is_=False):
    return get_url(f'{web}get-posts/{try_int(lng, 1)}{"?" if "?" not in web else ""}&search={query}')
  def fix_patch_notes(web, query, lng):
    resp = get_posts(web, query, lng)
    if resp and isinstance(resp, list) and isinstance(resp[0], dict):
      '''
      def _dict(_):
        _['url'] = f"{_['title']} · {web}news/{_['slug']}?lng={lng}"
        return _
      return [_dict(_) for _ in resp if 'title' in _ and 'slug' in _]
      '''
      return [{**_, **{'url': f"{_['title']} · {website}news/{_['slug']}?lng={lng.lang_code if hasattr(lng, 'lang_code') else lng}"}} for _ in resp if 'title' in _]# and 'slug' in _
      '''
      for _ in resp:
        if 'title' in _ and 'slug' in _:
          print(_)
          #_ is dict
          resp[_]['url'] = f"{resp[_]['title']} · {web}news/{resp[_]['slug']}?lng={lng}"
          #''.join([resp[_]['title'], ' · ', web, 'news/', resp[_]['slug'], '?lng=', lng])
      '''
    return resp
  website, website_api = get_links(blueprint)
  if website_api:
    _posts = get_posts(website_api, 'update%20notes')
    if _posts and isinstance(_posts, list) and len(_posts) > 0:
      _title = _posts[0]['slug'].replace('-', '%20') if use_slug else _posts[0]['title'][:_posts[0]['title'].rfind('update') - 1]
      _patchs = fix_patch_notes(website_api, _title, lang)
      if _patchs and isinstance(_patchs, list) and len(_patchs) > 0:
        if requested_json:
          return _patchs
        return _patchs[-1]['url']
  return f'{website}news/?lng={lang.lang_code}'

'''
from utils.http import get_url
'https://cms.smitegame.com/wp-json/smite-api/'
'https://www.smitegame.com/'
def patch_notes_func(website_api='https://cms.paladins.com/wp-json/api/', website='https://paladins.com/', lang=None):
  _updates_posts = get_url(f'{website_api}get-posts/1?&search=update%20notes')
  if _updates_posts and isinstance(_updates_posts, list) and len(_updates_posts) > 0:
    _title = _updates_posts[0]['title']
    _patch_notes = get_url(f'{website_api}get-posts/1?&search={_title[:_title.rfind("update") - 1]}')
    if _patch_notes and isinstance(_patch_notes, list) and len(_patch_notes) > 0:
      _patch_notes = _patch_notes[-1]
      return f"{_patch_notes['title']} - {website}news/{_patch_notes['slug']}?lng={lang}"
  return f'{website}news/?lng={lang}'

#Our Darkness & Dragons Update is LIVE on all platforms! Be sure to visit our update notes on Paladins.com for all the PTS changes & adjustments: paladins.com/news/darkness-dragons-update-notes
'''
