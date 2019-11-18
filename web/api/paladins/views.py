#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

if not hasattr(blueprint, 'paladins_api'):
	from pyrez.api import PaladinsAPI
	from utils import get_env
	blueprint.paladins_api = PaladinsAPI(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID'))

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
from utils.flask import get_player_id, get

#from flask import request

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler():
	"""Homepage route."""
	return str(blueprint.paladins_api.ping())

@blueprint.route('/deck', methods=['GET'], strict_slashes=False)
@blueprint.route('/decks', methods=['GET'], strict_slashes=False)
def decks_handler():
	return get_page()

@blueprint.route('/winrate', methods=['GET'], strict_slashes=False)
@blueprint.route('/kda', methods=['GET'], strict_slashes=False)
def kda_handler():
	return get_page()

@blueprint.route('/lastmatch', methods=['GET'], strict_slashes=False)
@blueprint.route('/last_match', methods=['GET'], strict_slashes=False)
def lastmatch_handler():
	return get_page()

@blueprint.route('/currentmatch', methods=['GET'], strict_slashes=False)
@blueprint.route('/current_match', methods=['GET'], strict_slashes=False)
@blueprint.route('/livematch', methods=['GET'], strict_slashes=False)
@blueprint.route('/live_match', methods=['GET'], strict_slashes=False)
def livematch_handler():
	return get_page()

@blueprint.route('/rank', methods=['GET'], strict_slashes=False)
def rank_handler():
	#from flask import url_for
	#print(url_for('api.paladins.views.rank_handler', external=True)) > /api/paladins/rank/?external=True
	#print(url_for('api.paladins.views.rank_handler', external=True, _external=True))
	return str(get_player_id(player_name=get('player'), _db_model=Paladins, _api=blueprint.paladins_api, platform=get('platform', 'pc')))
@blueprint.route('/stalk', methods=['GET'], strict_slashes=False)
def stalk_handler():
	return get_page()

@blueprint.route('/version', methods=['GET'], strict_slashes=False)
def version_handler():
	from .controllers.version import func
	from utils.flask import get_lang_id
	return func(as_json='json' in get('format', '') or get('json'), _api=blueprint.paladins_api, lang=get_lang_id())
	#return get_page()
