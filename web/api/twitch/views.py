#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint, is_async

#blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))
blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def get_page():
	if is_async():
		from quart import request
	else:
		from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

if is_async():
	@blueprint.route('/', methods=['GET'])
	async def root_handler(error=None):
		"""Homepage route."""
		from quart import jsonify, current_app
		from urllib.parse import unquote
		return jsonify([_ for _ in sorted(unquote('{:50s} {:20s} {}'.format(r.endpoint, ','.join(r.methods), r)) for r in current_app.url_map.iter_rules())])

	@blueprint.route('/random_viewer/', methods=['GET'])
	async def random_viewer_handler():
		return get_page()
else:
	@blueprint.route('/', methods=['GET'])
	def root_handler(error=None):
		"""Homepage route."""
		return get_page()

	@blueprint.route('/random_viewer/', methods=['GET'])
	def random_viewer_handler():
		return get_page()
