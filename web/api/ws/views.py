#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import is_async
if False:#is_async():
	from utils.web import create_blueprint
	blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', template_folder='templates', url_prefix='/{}'.format('/'.join(__name__.split('.')[1:-1])))

	@blueprint.route('/', strict_slashes=False)
	async def index():
		"""https://github.com/pgjones/quart/blob/master/docs/websockets.rst"""
		from quart import render_template
		return await render_template('{}/index.html'.format(__name__.split('.')[-2]))
