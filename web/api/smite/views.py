#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint
blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format('/'.join(__name__.split('.')[1:-1])))

if not hasattr(blueprint, '__api__'):
	import pyrez
	from utils import get_env
	blueprint.__api__ = getattr(pyrez, '{}API'.format(__name__.split('.')[-2].capitalize()))(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID'))

from utils.web import get, decorators
from utils.web.exceptions import PlayerRequired

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	"""Homepage route."""
	return str(blueprint.__api__.ping())

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
	return get_page()

@blueprint.route('/stalk', methods=['GET'], strict_slashes=False)
@decorators.player_required
def stalk_handler():
	return get_page()

@blueprint.route('/version', methods=['GET'], strict_slashes=False)
def version_handler():
	return get_page()
