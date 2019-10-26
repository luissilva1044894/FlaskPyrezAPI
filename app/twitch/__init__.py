#!/usr/bin/env python
# -*- coding: utf-8 -*-

def register(app):
	from .views import blueprint

	app.register_blueprint(blueprint, url_prefix='/{}'.format(__name__.replace('app.', 'api/')))
