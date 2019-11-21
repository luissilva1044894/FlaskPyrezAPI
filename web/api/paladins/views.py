#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

if not hasattr(blueprint, '__api__'):
	#setattr(self, credential.replace('.', '_'), os.getenv(credential))
	#getattr(self.__class__, 'query').filter_by(id=self.id).first().delete()
	import pyrez
	from utils import get_env
	blueprint.__api__ = getattr(pyrez, '{}API'.format(__name__.split('.')[-2].capitalize()))(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID'))
'''
@blueprint.before_app_first_request
@blueprint.before_app_request
@blueprint.before_request
def before_app_first_request_func():
	print('before_app_request')
@blueprint.app_errorhandler(404) #https://stackoverflow.com/questions/12768825/flask-error-handler-for-blueprints
def app_errorhandler(error=None):
	from flask import request
	if request.full_path.rfind(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')) != -1:
		return error
	return '?'
'''
from ...models.player import Paladins
from utils import flask
from utils.flask import get_player_id, get, get_lang_id
import requests
from flask import g

@blueprint.errorhandler(requests.exceptions.ConnectionError)
def connection_error_handler(error=None):
	return 'Internal Error!'

@blueprint.errorhandler(flask.exceptions.PlayerRequired)
def player_required_error_handler(error=None):
	return f"🚫 ERROR: No player name!."

@blueprint.errorhandler(flask.exceptions.ChampRequired)
def champ_required_error_handler(error=None):
	return f"🚫 ERROR: No champ name!."

@blueprint.errorhandler(flask.exceptions.NoDeck)
def no_deck_error_handler(error=None):
	return f"🚫 ERROR: “{g.__player__}” doesn't have any “{g.__champ__}” custom loadouts!."

@blueprint.errorhandler(flask.exceptions.NoChamp)
def no_champ_error_handler(error=None):
	return f"🚫 ERROR: Invalid champ name “{g.__champ__}”!"

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler():
	"""Homepage route."""
	return str(blueprint.__api__.ping())

@blueprint.route('/decks', methods=['GET'], strict_slashes=False)
@flask.decorators.player_required
@flask.decorators.champ_required
def decks_handler():
	from .controllers.decks import func

	_player_id = get_player_id(player_name=get('player'), _db_model=Paladins, _api=blueprint.__api__, platform=get('platform', 'pc'))
	__rt = func(get('champ', ''), player_id=_player_id, _api=blueprint.__api__, lang=get('lang', get_lang_id()), nodeck_exc=flask.exceptions.NoDeck, nochamp_exc=flask.exceptions.NoChamp)
	if isinstance(__rt, dict):
		from flask import jsonify
		return jsonify(__rt)
	return str(__rt)
	return get_page()

@blueprint.route('/kda', methods=['GET'], strict_slashes=False)
@flask.decorators.player_required
def kda_handler():
	return get_page()

@blueprint.route('/last_match', methods=['GET'], strict_slashes=False)
@flask.decorators.player_required
def lastmatch_handler():
	return get_page()

@blueprint.route('/live_match', methods=['GET'], strict_slashes=False)
@flask.decorators.player_required
def livematch_handler():
	return get_page()

@blueprint.route('/rank', methods=['GET'], strict_slashes=False)
@flask.decorators.player_required
def rank_handler():
	#from flask import url_for
	#print(url_for('api.paladins.views.rank_handler', external=True)) > /api/paladins/rank/?external=True
	#print(url_for('api.paladins.views.rank_handler', external=True, _external=True))
	return str(get_player_id(player_name=get('player'), _db_model=Paladins, _api=blueprint.__api__, platform=get('platform', 'pc')))
@blueprint.route('/stalk', methods=['GET'], strict_slashes=False)
@flask.decorators.player_required
def stalk_handler():
	return get_page()

@blueprint.route('/version', methods=['GET'], strict_slashes=False)
def version_handler():
	from .controllers.version import func
	return func(as_json='json' in get('format', '') or get('json'), _api=blueprint.__api__, lang=get('lang', get_lang_id()))
	#return get_page()
