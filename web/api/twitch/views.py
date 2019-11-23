#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from flask import Blueprint
from utils import create_blueprint
from utils import replace

#blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))
blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

'''
from utils import supports_quart
if supports_quart:
	def get_page():
		from quart import request
		return ' '.join([blueprint.name, request.url_rule.rule])

	@blueprint.route('/', methods=['GET'])
	async def root_handler(error=None):
		"""Homepage route."""
		return get_page()

		@blueprint.route('/random_viewer/', methods=['GET'])
		@blueprint.route('/random_user/', methods=['GET'])
		async def random_viewer_handler():
			return get_page()
else:
	def get_page():
		from flask import request
		return ' '.join([blueprint.name, request.url_rule.rule])

	@blueprint.route('/', methods=['GET'])
	def root_handler(error=None):
		"""Homepage route."""
		return get_page()

	@blueprint.route('/random_viewer/', methods=['GET'])
	@blueprint.route('/random_user/', methods=['GET'])
	def random_viewer_handler():
		return get_page()
'''
def get_page():
	import quart
	if isinstance(blueprint, quart.Blueprint):
		from quart import request
	else:
		from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	"""Homepage route."""
	return get_page()

@blueprint.route('/random_viewer/', methods=['GET'])
@blueprint.route('/random_user/', methods=['GET'])
def random_viewer_handler():
	return get_page()
