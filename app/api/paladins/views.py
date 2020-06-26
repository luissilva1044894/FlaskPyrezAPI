#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from .controllers import (
  decks,
  kda,
  live_match,
  patch_notes,
  rank,
  stalk,
  version,
)
from utils.hirez.patch_notes import get_patch_notes
from utils import web

paladins = web.create_blueprint(__name__, static_folder='static')#, template_folder='templates'

@paladins.errorhandler(requests.exceptions.ConnectionError)
@paladins.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  print(error)
  return '🚫 ERROR: An unexpected error has occurred!'

@paladins.errorhandler(web.exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@paladins.errorhandler(404)
@paladins.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return web.get_page(paladins)

@paladins.route('/decks', methods=['GET'])
@web.decorators.field_required(field=['champ', 'champ_id', 'champ_name'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _decks_route_():
  """Decks of a champion"""
  return decks.decks_func()

@paladins.route('/kda', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
@web.decorators.field_required(field=['champ', 'champ_id', 'champ_name'], surpress_exceptions=True)
def _kda_route_():
  """KDA of a player or champion"""
  return kda.kda_func()

@paladins.route('/last_match', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _last_match_route_():
  """Get information about a previously finished match"""
  return '?'

@paladins.route('/live_match', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _live_match_route_():
  """All players rank in a live match"""
  return live_match.live_match_func()

@paladins.route('/patch_notes', methods=['GET'])
def _patch_notes_route_():
  return get_patch_notes(website_api='https://cms.paladins.com/wp-json/api/', website='https://www.paladins.com/', lang=None)
  #return patch_notes.patch_notes_func()

@paladins.route('/rank', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _rank_route_():
  """Currently rank of a specified player"""
  return rank.rank_func()

@paladins.route('/stalk', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _stalk_route_():
  """Currently online status of a specified player"""
  return stalk.stalk_func()

@paladins.route('/version', methods=['GET'])
def _version_route_():
  """Currently status of Paladins Server"""
  return version.version_func()
