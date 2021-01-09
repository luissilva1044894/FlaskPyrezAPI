#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
  from httpx import Client
except ImportError:
  from requests import Session as Client

from .base_api import BaseAPI

class API(BaseAPI):
  def make_request(self, method_name, params=None, *args, **kw):
    method_name = str(method_name).lower()
    if not self.session_id and not 'createsession' in method_name:
      self.session = self.create_session()

    url = self.build_request_url(method_name, params)
    with Client() as session:
      try:
        with session.get(url, *args, **kw) as r:
          pass
      except AttributeError:
        r = session.get(url, *args, **kw)
      finally:
        return r.json() if 'json' in r.headers.get('Content-Type', '') else r.text

  def create_session(self, *args, **kw):
    return self.make_request('createsession', *args, **kw)

  def get_champion_cards(self, god_id, lang=None, *args, **kw):
    return self.make_request('getchampioncards', params=[god_id, lang or 1], *args, **kw)

  def get_data_used(self, *args, **kw):
    return self.make_request('getdataused', *args, **kw)

  def get_demo_details(self, match_id, *args, **kw):
    return self.make_request('getdemodetails', params=match_id, *args, **kw)

  def get_esports_pro_league_details(self, *args, **kw):
    return self.make_request('getesportsproleaguedetails', *args, **kw)

  def get_friends(self, player_id, *args, **kw):
    return self.make_request('getfriends', params=player_id, *args, **kw)

  def get_god_leaderboard(self, god_id, queue_id, *args, **kw):
    #getChampionLeaderboard
    return self.make_request('getgodleaderboard', params=[god_id, queue_id], *args, **kw)

  def get_god_ranks(self, player_id, god_id, *args, **kw):
    #getChampionRanks
    return self.make_request('getgodranks', params=[player_id, god_id], *args, **kw)

  def get_god_recommended_items(self, god_id, lang=None, *args, **kw):
    return self.make_request('getgodrecommendeditems', params=[god_id, lang or 1], *args, **kw)

  def get_gods(self, lang=None, *args, **kw):
    #getChampions
    return self.make_request('getgods', params=lang or 1, *args, **kw)

  def get_god_skins(self, god_id, lang=None, *args, **kw):
    #getChampionSkins
    return self.make_request('getgodskins', params=[god_id, lang or 1], *args, **kw)

  def get_hirez_server_status(self, *args, **kw):
    return self.make_request('gethirezserverstatus', *args, **kw)

  def get_items(self, lang=None, *args, **kw):
    return self.make_request('getitems', params=lang or 1, *args, **kw)

  def get_leaderboard (self, queue_id, ranking_criteria, *args, **kw):
    return self.make_request('getleaderboard', params=[queue_id, ranking_criteria], *args, **kw)

  def get_league_leaderboard(self, queue_id, tier, split, *args, **kw):
    return self.make_request('getleagueleaderboards', params=[queue_id, tier, split], *args, **kw)

  def get_league_seasons(self, queue_id, *args, **kw):
    return self.make_request('getleagueseasons', params=queue_id, *args, **kw)

  def get_match_details(self, match_id, *args, **kw):
    return self.make_request('getmatchdetails', params=match_id, *args, **kw)

  def get_match_details_batch(self, match_ids, *args, **kw):
    if kw.pop('sorted', None):
      return self.make_request('getmatchdetailsbatchsorted', params=match_ids, *args, **kw)  
    return self.make_request('getmatchdetailsbatch', params=match_ids, *args, **kw)

  def get_match_history(self, player_id, *args, **kw):
    return self.make_request('getmatchhistory', params=player_id, *args, **kw)

  def get_match_ids_by_queue(self, queue_id, date, hour=-1, *args, **kw):
    return self.make_request('getmatchidsbyqueue', params=[queue_id, date, hour], *args, **kw)

  def get_match_player_details(self, match_id, *args, **kw):
    return self.make_request('getmatchplayerdetails', params=match_id, *args, **kw)

  def get_motd(self, *args, **kw):
    return self.make_request('getmotd', *args, **kw)

  def get_patch_info(self, *args, **kw):
    return self.make_request('getpatchinfo', *args, **kw)

  def get_player(self, player, portal_id=None, *args, **kw):
    if portal_id:
      return self.make_request('getplayer', params=[player, portal_id], *args, **kw)
    return self.make_request('getplayer', params=player, *args, **kw)

  def get_player_achievements(self, player_id, *args, **kw):
    return self.make_request('getplayerachievements', params=player_id, *args, **kw)

  def get_player_batch(self, player_ids, *args, **kw):
    return self.make_request('getplayerbatch', params=player_ids, *args, **kw)

  def get_player_batch_from_match(self, match_id, *args, **kw):
    return self.make_request('getplayerbatchfrommatch', params=match_id, *args, **kw)

  def get_player_champions(self, player_id, *args, **kw):
    return self.make_request('getplayerchampions', params=player_id, *args, **kw)

  def get_player_id_by_name(self, player, *args, **kw):
    return self.make_request('getplayeridbyname', params=player, *args, **kw)

  def get_player_id_by_portal_user_id(self, portal_id, portal_user_id, *args, **kw):
    return self.make_request('getplayeridbyportaluserid', params=[portal_id, portal_user_id], *args, **kw)

  def get_player_id_info_for_xbox_and_switch(self, player, *args, **kw):
    return self.make_request('getplayeridinfoforxboxandswitch', params=player, *args, **kw)

  def get_player_ids_by_gamertag(self, portal_id, gamer_tag, *args, **kw):
    return self.make_request('getplayeridsbygamertag', params=[portal_id, gamer_tag], *args, **kw)

  def get_player_loadouts(self, player_id, lang=None, *args, **kw):
    return self.make_request('getplayerloadouts', params=[player_id, lang or 1], *args, **kw)

  def get_player_match_history(self, player_id, *args, **kw):
    return self.make_request('getplayermatchhistory', params=player_id, *args, **kw)

  def get_player_stats(self, player_id, *args, **kw):
    return self.make_request('getplayerstats', params=player_id, *args, **kw)

  def get_player_status(self, player_id, *args, **kw):
    return self.make_request('getplayerstatus', params=player_id, *args, **kw)

  def get_queue_stats(self, player_id, queue_id, *args, **kw):
    return self.make_request('getqueuestats', params=[player_id, queue_id], *args, **kw)

  def get_talents(self, lang=None, *args, **kw):
    return self.make_request('gettalents', params=lang or 1, *args, **kw)

  def get_team_details(self, team_id, *args, **kw):
    return self.make_request('getteamdetails', params=team_id, *args, **kw)

  def get_team_match_history(self, team_id, *args, **kw):
    return self.make_request('getteammatchhistory', params=team_id, *args, **kw)

  def get_team_players(self, team_id, *args, **kw):
    return self.make_request('getteamplayers', params=team_id, *args, **kw)

  def get_top_matches(self, *args, **kw):
    return self.make_request('gettopmatches', *args, **kw)

  def ping(self, *args, **kw):
    return self.make_request('ping', *args, **kw)

  def search_players(self, player, *args, **kw):
    return self.make_request('searchplayers', params=player, *args, **kw)

  def search_teams(self, team_name, *args, **kw):
    return self.make_request('searchteams', params=team_name, *args, **kw)

  def test_session(self, session_id=None, *args, **kw):
    url = self.endpoint + '/'.join([method_name + 'testsessionjson', self.dev_id, self.create_signature(method_name), session_id or self.session_id, self.create_timestamp()])
    with Client() as session:
      try:
        with session.get(url, *args, **kw) as r:
          pass
      except AttributeError:
         r = session.get(url, *args, **kw)
      finally:
        if r.status == 200:
          return 'successful' in r.json()
