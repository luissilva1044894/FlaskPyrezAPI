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

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler():
	"""Homepage route."""
	return str(blueprint.paladins_api.ping())

@blueprint.route('/deck', methods=['GET'])
@blueprint.route('/decks', methods=['GET'])
def decks_handler():
	return get_page()

@blueprint.route('/winrate', methods=['GET'])
@blueprint.route('/kda', methods=['GET'])
def kda_handler():
	return get_page()

@blueprint.route('/lastmatch', methods=['GET'])
@blueprint.route('/last_match', methods=['GET'])
def lastmatch_handler():
	return get_page()

@blueprint.route('/currentmatch', methods=['GET'])
@blueprint.route('/current_match', methods=['GET'])
@blueprint.route('/livematch', methods=['GET'])
@blueprint.route('/live_match', methods=['GET'])
def livematch_handler():
	return get_page()

@blueprint.route('/rank/', methods=['GET'])
def rank_handler():
	#from flask import url_for
	#print(url_for('api.paladins.views.rank_handler', external=True)) > /api/paladins/rank/?external=True
	#print(url_for('api.paladins.views.rank_handler', external=True, _external=True))
	return get_page()

@blueprint.route('/stalk', methods=['GET'])
def stalk_handler():
	return get_page()

@blueprint.route('/version', methods=['GET'])
def version_handler():
	return get_page()
