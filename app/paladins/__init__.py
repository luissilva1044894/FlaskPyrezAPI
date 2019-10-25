#!/usr/bin/env python
# -*- coding: utf-8 -*-

def register_app(app):
	from .views import paladins

	app.register_blueprint(paladins, url_prefix='/paladins')
	app.register_blueprint(paladins, url_prefix='/api')

	return app
