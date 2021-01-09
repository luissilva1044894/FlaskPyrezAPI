#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
try:
  from httpx import AsyncClient as Client
except ImportError:
  from aiohttp import ClientSession as Client
"""
from aiohttp import ClientSession as Client

from .base_api import BaseAPI

class AsyncAPI(BaseAPI):
  async def make_request(self, method_name, params=None, *args, **kw):
    async def json_or_text(resp):
      try:
        if 'json' in resp.headers.get('Content-Type', ''):
          return await resp.json()
        return await resp.text()
      except TypeError:
        return resp.json() if 'json' in resp.headers.get('Content-Type', '') else resp.text
    method_name = str(method_name).lower()
    if not self.session_id and not 'createsession' in method_name:
      self.session = await self.create_session()

    url = self.build_request_url(method_name, params)
    async with Client() as session:
      try:
        async with session.get(url, *args, **kw) as r:
          return await json_or_text(r)
      except AttributeError:
        r = await session.get(url)
        return await json_or_text(r)

  async def create_session(self, *args, **kw):
    return await self.make_request('createsession', *args, **kw)

  async def get_champion_cards(self, god_id, lang=None, *args, **kw):
    return await self.make_request('getchampioncards', params=[god_id, lang or 1], *args, **kw)

  async def get_data_used(self, *args, **kw):
    return await self.make_request('getdataused', *args, **kw)

  async def get_demo_details(self, match_id, *args, **kw):
    return await self.make_request('getdemodetails', match_id, *args, **kw)

  async def get_esports_pro_league_details(self, *args, **kw):
    return await self.make_request('getesportsproleaguedetails', *args, **kw)

  async def get_friends(self, player_id, *args, **kw):
    return await self.make_request('getfriends', player_id, *args, **kw)

  async def get_god_leaderboard(self, god_id, queue_id, *args, **kw):
    return await self.make_request('getgodleaderboard', [god_id, queue_id], *args, **kw)

  async def get_god_ranks(self, player_id, god_id):
    return await self.make_request('getgodranks', [player_id, god_id])

  async def get_god_recommended_items(self, god_id):
    return await self.make_request('getgodrecommendeditems', [god_id, lang or 1])

  async def get_god_skins(self, god_id, lang=None):
    return await self.make_request('getgodskins', [god_id, lang or 1])

  async def get_gods(self, lang=None):
    return await self.make_request('getgods', lang or 1)

  async def get_hirez_server_status(self):
    return await self.make_request('gethirezserverstatus')

  async def get_items(self, lang=None):
    return await self.make_request('getitems', lang or 1)

  async def get_leaderboard(self, queue_id, ranking_criteria, *args, **kw):
    return await self.make_request('getleaderboard', params=[queue_id, ranking_criteria], *args, **kw)

  async def get_league_leaderboard(self, queue_id, tier, season):
    return await self.make_request('getleagueleaderboards', [queue_id, tier, season])

  async def get_league_seasons(self, queue_id):
    return await self.make_request('getleagueseasons', queue_id)

  async def get_match_details(self, match_id):
    return await self.make_request('getmatchdetails', match_id)

  async def get_match_details_batch(self, match_ids):
    if kw.pop('sorted', None):
      return await self.make_request('getmatchdetailsbatchsorted', params=match_ids, *args, **kw)  
    return await self.make_request('getmatchdetailsbatch', params=match_ids, *args, **kw)

  async def get_match_history(self, player_id):
    return await self.make_request('getmatchhistory', player_id)

  async def get_match_ids_by_queue(self, queue_id, date, hour=-1):
    return await self.make_request('getmatchidsbyqueue', [queue_id, date, hour])

  async def get_match_player_details(self, match_id):
    return await self.make_request('getmatchplayerdetails', match_id)

  async def get_motd(self):
    return await self.make_request('getmotd')

  async def get_patch_info(self):
    return await self.make_request('getpatchinfo')

  async def get_player(self, player, portal_id=None, *args, **kw):
    if portal_id:
      return await self.make_request('getplayer', params=[player, portal_id], *args, **kw)
    return await self.make_request('getplayer', player)

  async def get_player_achievements(self, player_id):
    return await self.make_request('getplayerachievements', player_id)

  async def get_player_batch(self, player_ids, *args, **kw):
    return await self.make_request('getplayerbatch', params=player_ids, *args, **kw)

  async def get_player_batch_from_match(self, match_id, *args, **kw):
    return await self.make_request('getplayerbatchfrommatch', params=match_id, *args, **kw)

  async def get_player_champions(self, player_id, *args, **kw):
    return await self.make_request('getplayerchampions', params=player_id, *args, **kw)

  async def get_player_id_by_name(self, player):
    return await self.make_request('getplayeridbyname', player)

  async def get_player_id_by_portal_user_id(self, portal_id, portal_user_id):
    return await self.make_request('getplayeridbyportaluserid', [portal_id, portal_user_id])

  async def get_player_id_info_for_xbox_and_switch(self, player, *args, **kw):
    return await self.make_request('getplayeridinfoforxboxandswitch', params=player, *args, **kw)

  async def get_player_ids_by_gamertag(self, portal_id, gamer_tag):
    return await self.make_request('getplayeridsbygamertag', [portal_id, gamer_tag])

  async def get_player_loadouts(self, player_id, lang=None, *args, **kw):
    return await self.make_request('getplayerloadouts', params=[player_id, lang or 1], *args, **kw)

  async def get_player_match_history(self, player_id, *args, **kw):
    return await self.make_request('getplayermatchhistory', params=player_id, *args, **kw)

  async def get_queue_stats(self, player_id, queue_id):
    return await self.make_request('getqueuestats', queue_id)

  async def get_player_status(self, player_id):
    return await self.make_request('getplayerstatus', player_id)

  async def get_queue_stats(self, player_id, queue_id, *args, **kw):
    return await self.make_request('getqueuestats', params=[player_id, queue_id], *args, **kw)

  async def get_talents(self, lang=None, *args, **kw):
    return await self.make_request('gettalents', params=lang or 1, *args, **kw)

  async def get_team_details(self, team_id):
    return await self.make_request('getteamdetails', team_id)

  async def get_team_match_history(self, team_id, *args, **kw):
    return await self.make_request('getteammatchhistory', params=team_id, *args, **kw)

  async def get_team_players(self, team_id):
    return await self.make_request('getteamplayers', team_id)

  async def get_top_matches(self):
    return await self.make_request('gettopmatches')

  async def ping(self):
    return await self.make_request('ping')

  async def search_players(self, player):
    return await self.make_request('searchplayers', player)

  async def search_teams(self, team_name, *args, **kw):
    return await self.make_request('searchteams', team_name, *args, **kw)

  async def test_session(self, session_id=None, *args, **kw):
    url = self.endpoint + '/'.join([method_name + 'testsessionjson', self.dev_id, self.create_signature(method_name), session_id or self.session_id, self.create_timestamp()])
    async with Client() as session:
      async with session.get(url, *args, **kw) as r:
        if r.status == 200:
          return 'successful' in await r.json()
