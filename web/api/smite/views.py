#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	"""Homepage route."""
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
	return get_page()

@blueprint.route('/stalk', methods=['GET'])
def stalk_handler():
	return get_page()

@blueprint.route('/version', methods=['GET'])
def version_handler():
	return get_page()
