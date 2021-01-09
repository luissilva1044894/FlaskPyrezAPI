#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  g,
  render_template,
  request,
)
import pyrez
from pyrez import PaladinsAPI
import requests

from utils import environ
from utils.hirez import (
  decks,
  kda,
  live_match,
  patch_notes,
  rank,
  stalk,
  version,
)
from utils.hirez.api import API
from utils.hirez.enums.platform import get_platform
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)
paladins = create_blueprint(__name__, static_folder='static')#, template_folder='templates'

@paladins.before_request
def before_request_handler():
  pass
  #Testa se a key é igual o hash, se não: raise. Else: faz nada

@paladins.before_app_first_request
def before_app_first_request_handler():
  paladins.paladins_api = pyrez.PaladinsAPI(environ.get_env('PYREZ_DEV_ID'), environ.get_env('PYREZ_AUTH_ID'))
  #paladins.api = API(environ.get_env('PYREZ_DEV_ID'), environ.get_env('PYREZ_AUTH_ID'), 'http://api.paladins.com/paladinsapi.svc')
  #Lê o JSON e salva no g.

@paladins.errorhandler(requests.exceptions.ConnectionError)
@paladins.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

'''
@paladins.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error.message}'
'''

@paladins.errorhandler(pyrez.exceptions.PlayerNotFound)
def player_not_found_error_handler(error=None):
  return f"🚫 ERROR: “{g.player}” doesn't exist! Quotation marks required if the “player_name” contains spaces."

@paladins.errorhandler(pyrez.exceptions.MatchException)
@paladins.errorhandler(pyrez.exceptions.PrivatePlayer)
def private_player_error_handler(error=None):
  return f"🔒 ERROR: “{g.player}” it's hidden! Make sure that your account is marked as “Public Profile”."

@paladins.errorhandler(pyrez.exceptions.ServiceUnavailable)
def service_unavailable_error_handler(error=None):
  return '🚫 ERROR: Unable to connect to Hi-Rez Studios API!'

@paladins.errorhandler(pyrez.exceptions.MatchException)
def service_unavailable_error_handler(error=None):
  return '🚫 ERROR: Unable to connect to Hi-Rez Studios API!'
  #QUEUE_ID_NOT_SUPPORTED_STRINGS[language].format(QUEUE_IDS_STRINGS[lang][player_status_request.queueId], player)

@paladins.errorhandler(404)
@paladins.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(paladins)

@paladins.route('/decks', methods=['GET'])
@decorators.field_required(field=['champ', 'champ_id', 'champ_name'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _decks_route_():
  """Decks of a champion"""
  return decks.decks_func(player=g.player, champ=g.champ, platform=g.platform, lang='en' or g.language, api=paladins.paladins_api)

@paladins.route('/kda', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['champ', 'champ_id', 'champ_name'], surpress_exceptions=True)
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _kda_route_():
  """Displays the KDA of a player or champion with the wins/losses & winrate."""
  return kda.kda_func(player=g.player, champ=g.champ, platform=g.platform, lang='en' or g.language, api=paladins.paladins_api)

@paladins.route('/last_match', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _last_match_route_():
  """Displays statistics about a previously finished match"""
  #Match details for the provided `MatchID` or latest match played of provided `PlayerName`.
  #Latest match history for `PlayerName`.
  print(g.platform, int(g.platform), str(g.platform))
  return str(g.__dict__)

@paladins.route('/live_match', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
#@decorators.field_required(field=['channel', 'channel_id'])
#@decorators.field_required(field=['key'])
#@decorators.require_key()
def _live_match_route_():
  """Shows the ranks of player in a live match"""
  #Match details if provided `PlayerName` is in a match.
  #http://127.0.0.1:5000/api/paladins/hash?channel=mittow&key=zif9a7sKKpqCZsLsKWfBNlhTaAC1mG41mrOA_bmj3mo
  #http://127.0.0.1:5000/api/paladins/hash?channel=mittow&key=zif9a7sKKpqCZsLsKWfBNlhTaAC1mG41mrOA_bmj3mo@ced928737652e8464bc8add9e85e6859
  return live_match.live_match_func(player=g.player, platform=g.platform, lang='en' or g.language, api=paladins.paladins_api)

@paladins.route('/patch_notes', methods=['GET'])
def _patch_notes_route_():
  """Latest Patch Notes"""
  return patch_notes.get_patch_notes(blueprint=paladins, lang=g.language, requested_json=g.requested_json)

'''
@paladins.route('/hash', methods=['GET'])
def _hash_route_():
  def _(o, encoding='utf-8'):
    if hasattr(o, 'decode'):
      return o.decode(encoding=encoding)
    try:
      return str(o, encoding=encoding or 'latin-1')
    except (TypeError, ValueError):
      return o
  if '@' in g.key:
    key, hash_ = g.key.split('@')
    _msg = encrypt(hashing(g.channel, key), key)
    return f'{_(hashing(g.channel, key))} \r\n\r\n{_(_msg)} \r\n\r\n{_(decrypt(_msg, key))} \r\n\r\n{decrypt(_msg, key) == hash_.encode()}'
  _msg = encrypt(hashing(g.channel, g.key), g.key)
  return f'{_(_msg)} \r\n\r\n{_(decrypt(_msg, g.key))}'
'''

@paladins.route('/rank', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _rank_route_():
  """Displays the current rank of a specified player"""
  return rank.rank_func(player=g.player, platform=g.platform, lang='en' or g.language, api=paladins.paladins_api)

@paladins.route('/stalk', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _stalk_route_():
  """Currently online status of a specified player"""
  return stalk.stalk_func(player=g.player, platform=g.platform, lang='en' or g.language, api=paladins.paladins_api)

@paladins.route('/version', methods=['GET'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _version_route_():
  """Currently status of Paladins Server"""
  print(paladins.paladins_api.ping())
  return version.get_version(platform=g.platform, api=paladins.paladins_api, blueprint=paladins, requested_json=g.requested_json)
