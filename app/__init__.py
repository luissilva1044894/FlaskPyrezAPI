# -*- coding: utf-8 -*-

#https://danidee10.github.io/2016/11/20/flask-by-example-8.html
#https://exploreflask.com/en/latest/blueprints.html
#https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/#internationalized-blueprint-urls
#https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/

def register(app):
	from .views import blueprint
	from .utils import replace
	app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app', 'api')))

	import os
	os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
	import importlib
	for _mod in [_ for _ in os.listdir('.') if os.path.isdir(_) and not _.startswith('_')]:
		try:
			_lib = importlib.import_module('.'.join([__name__, _mod]))
		except ModuleNotFoundError:
			pass
		else:
			try:
				_lib.register(app)
			except AttributeError:
				pass
