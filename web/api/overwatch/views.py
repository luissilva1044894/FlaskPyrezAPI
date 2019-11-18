#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

#print(f'Path: {__name__}', 'Name: %s' % __name__.split('.')[-2])
blueprint = Blueprint(__name__.split('.', 1)[-1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	"""Homepage route."""
	return get_page()

@blueprint.route('/rank', methods=['GET'], strict_slashes=False)
def rank_handler():
	return get_page()
