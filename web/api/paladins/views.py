#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, jsonify, request, url_for
import pyrez
import requests

from .controllers.decks import func as decks_func
from .controllers.version import func as version_func
from ...models.paladins.player import Player
from utils import get_env
from utils.web import create_blueprint, decorators, exceptions, get, get_lang_id, get_player_id

blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format('/'.join(__name__.split('.')[1:-1])))

if not hasattr(blueprint, '__api__'):
	#setattr(self, credential.replace('.', '_'), os.getenv(credential))
	#getattr(self.__class__, 'query').filter_by(id=self.id).first().delete()
	print(pyrez.__version__)
  _cls_name = __name__.split('.')[-2].capitalize()
  if pyrez.__version__[:2] == '1.1':
  	_cls_name += 'API'
  blueprint.__api__ = getattr(pyrez, _cls_name)(get_env('PYREZ_DEV_ID'), get_env('PYREZ_AUTH_ID'))
  #blueprint.__api__ = getattr(pyrez, '{}'.format(__name__.split('.')[-2].capitalize()))(dev_id=get_env('PYREZ_DEV_ID'), auth_key=get_env('PYREZ_AUTH_ID')) < IndexError
'''
@blueprint.before_app_first_request
@blueprint.before_app_request
@blueprint.before_request
def before_app_first_request_func():
  print('before_app_request')
@blueprint.app_errorhandler(404) #https://stackoverflow.com/questions/12768825/flask-error-handler-for-blueprints
def app_errorhandler(error=None):
  if request.full_path.rfind(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')) != -1:
    return error
  return '?'
'''

@blueprint.errorhandler(requests.exceptions.ConnectionError)
@blueprint.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  return 'Internal Error!'

@blueprint.errorhandler(exceptions.PlayerRequired)
def player_required_error_handler(error=None):
  return '🚫 ERROR: No player name!.'

@blueprint.errorhandler(exceptions.ChampRequired)
def champ_required_error_handler(error=None):
  return '🚫 ERROR: No champ name!.'

@blueprint.errorhandler(exceptions.NoDeck)
def no_deck_error_handler(error=None):
  return f"🚫 ERROR: “{g.__player__}” doesn't have any “{g.__champ__}” custom loadouts!."

@blueprint.errorhandler(exceptions.NoChamp)
def no_champ_error_handler(error=None):
  return f"🚫 ERROR: Invalid champ name “{g.__champ__}”!"

def get_page():
  return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler():
  """Homepage route."""
  return str(blueprint.__api__.ping())

@blueprint.route('/decks', methods=['GET'], strict_slashes=False)
@decorators.player_required
@decorators.champ_required
@decorators.maybe_json
def decks_handler():
  _player_id = get_player_id(player_name=get('player'), _db_model=Player, _api=blueprint.__api__, platform=get('platform', 'pc'))
  return decks_func(get('champ', ''), player_id=_player_id, _api=blueprint.__api__, lang=get('lang', get_lang_id()), nodeck_exc=exceptions.NoDeck, nochamp_exc=exceptions.NoChamp)

@blueprint.route('/kda', methods=['GET'], strict_slashes=False)
@decorators.player_required
def kda_handler():
  return get_page()

@blueprint.route('/last_match', methods=['GET'], strict_slashes=False)
@decorators.player_required
def lastmatch_handler():
  return get_page()

@blueprint.route('/live_match', methods=['GET'], strict_slashes=False)
@decorators.player_required
def livematch_handler():
  return get_page()

@blueprint.route('/rank', methods=['GET'], strict_slashes=False)
@decorators.player_required
def rank_handler():
  #print(url_for('api.paladins.views.rank_handler', external=True)) > /api/paladins/rank/?external=True
  #print(url_for('api.paladins.views.rank_handler', external=True, _external=True))
  return str(get_player_id(player_name=get('player'), _db_model=Player, _api=blueprint.__api__, platform=get('platform', 'pc')))

@blueprint.route('/stalk', methods=['GET'], strict_slashes=False)
@decorators.player_required
def stalk_handler():
  return get_page()

@blueprint.route('/version', methods=['GET'], strict_slashes=False)
def version_handler():
  return version_func(as_json='json' in get('format', '') or get('json'), _api=blueprint.__api__, lang=get_lang_id(get('lang')))
