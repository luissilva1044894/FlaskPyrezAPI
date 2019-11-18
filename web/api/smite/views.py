#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

if not hasattr(blueprint, 'smite_api'):
	from pyrez.api import SmiteAPI
	from utils import get_env
	blueprint.smite_api = SmiteAPI(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID'))

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	"""Homepage route."""
	return str(blueprint.smite_api.ping())

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
	return get_page()

@blueprint.route('/stalk', methods=['GET'], strict_slashes=False)
def stalk_handler():
	return get_page()

@blueprint.route('/version', methods=['GET'], strict_slashes=False)
def version_handler():
	return get_page()
