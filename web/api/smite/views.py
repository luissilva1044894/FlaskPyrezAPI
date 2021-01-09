#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  g,
  render_template,
  request,
)
import pyrez
import requests

from utils.hirez import (
  kda,
  live_match,
  patch_notes,
  rank,
  stalk,
  version,
)
from utils.hirez.api import API
from utils.hirez.enums.platform import get_platform
from utils import environ
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)
smite = create_blueprint(__name__, static_folder='static')#, template_folder='templates'

@smite.before_request
def before_request_handler():
  pass

@smite.before_app_first_request
def before_app_first_request_handler():
  smite.smite_api = pyrez.SmiteAPI(environ.get_env('PYREZ_DEV_ID'), environ.get_env('PYREZ_AUTH_ID'))
  #smite.api = API(environ.get_env('PYREZ_DEV_ID'), environ.get_env('PYREZ_AUTH_ID'), 'http://api.paladins.com/paladinsapi.svc')

@smite.errorhandler(requests.exceptions.ConnectionError)
@smite.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  print(error)
  return '🚫 ERROR: An unexpected error has occurred!'

@smite.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@smite.errorhandler(pyrez.exceptions.PlayerNotFound)
def player_not_found_error_handler(error=None):
  return f"🚫 ERROR: “{g.player}” doesn't exist! Quotation marks required if the “player_name” contains spaces."

@smite.errorhandler(pyrez.exceptions.MatchException)
@smite.errorhandler(pyrez.exceptions.PrivatePlayer)
def private_player_error_handler(error=None):
  return f"🔒 ERROR: “{g.player}” it's hidden! Make sure that your account is marked as “Public Profile”."

@smite.errorhandler(pyrez.exceptions.ServiceUnavailable)
def service_unavailable_error_handler(error=None):
  return '🚫 ERROR: Unable to connect to Hi-Rez Studios API!'

@smite.errorhandler(pyrez.exceptions.MatchException)
def service_unavailable_error_handler(error=None):
  return '🚫 ERROR: Unable to connect to Hi-Rez Studios API!'
  #QUEUE_ID_NOT_SUPPORTED_STRINGS[language].format(QUEUE_IDS_STRINGS[lang][player_status_request.queueId], player)

@smite.errorhandler(404)
@smite.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(smite)

@smite.route('/kda', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['champ', 'champ_id', 'champ_name'], surpress_exceptions=True)
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _kda_route_():
  """KDA of a player or champion"""
  return kda.kda_func(player=g.player, champ=g.champ, platform=g.platform, lang='en' or g.language, api=smite.smite_api)

@smite.route('/last_match', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _last_match_route_():
  """Get information about a previously finished match"""
  print(g.platform, int(g.platform), str(g.platform))
  return str(g.__dict__)

@smite.route('/live_match', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _live_match_route_():
  """All players rank in a live match"""
  return live_match.live_match_func(player=g.player, platform=g.platform, lang='en' or g.language, api=smite.smite_api)

@smite.route('/patch_notes', methods=['GET'])
def _patch_notes_route_():
  """Get the latest Patch Notes"""
  return patch_notes.get_patch_notes(blueprint=smite, lang=g.language, requested_json=g.requested_json)

@smite.route('/rank', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _rank_route_():
  """Currently rank of a specified player"""
  return rank.rank_func(player=g.player, platform=g.platform, lang='en' or g.language, api=smite.smite_api)

@smite.route('/stalk', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _stalk_route_():
  """Currently online status of a specified player"""
  return stalk.stalk_func(player=g.player, platform=g.platform, lang='en' or g.language, api=smite.smite_api)

@smite.route('/version', methods=['GET'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _version_route_():
  """Currently status of Paladins Server"""
  return version.get_version(platform=g.platform, api=smite.smite_api, blueprint=smite, requested_json=g.requested_json)
