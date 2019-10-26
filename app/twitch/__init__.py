#!/usr/bin/env python
# -*- coding: utf-8 -*-

def register(app):
	from .views import blueprint

	from ..utils import replace
	app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app.', 'api/')))
