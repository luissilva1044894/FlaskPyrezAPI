#!/usr/bin/env python
# -*- coding: utf-8 -*-

def register(app):
	from .views import blueprint
	#print(blueprint.root_path)
	#input(app.root_path)
	#>>> simple_page.root_path
	#'/Users/username/TestProject/yourapplication'
	#with simple_page.open_resource('static/style.css') as f: #To quickly open sources from this folder you can use the open_resource() function:
	#    code = f.read()

	from ..utils import replace
	app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app.', 'api/')))
	#app.register_blueprint(blueprint, url_prefix='/api')

	#return app
