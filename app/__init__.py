# -*- coding: utf-8 -*-

#https://danidee10.github.io/2016/11/20/flask-by-example-8.html
#https://exploreflask.com/en/latest/blueprints.html
#https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/#internationalized-blueprint-urls
#https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/

#https://stackoverflow.com/questions/4239825/static-files-in-flask-robot-txt-sitemap-xml-mod-wsgi
def create_app():
	from flask import Flask
	from flask_sqlalchemy import SQLAlchemy
	from .utils import get_env
	import os

	def get_config(x=None):
		return {
			'development': 'config.DevelopementConfig',
            'dev': 'config.DevelopementConfig',
            'testing': 'config.TestingConfig',
            'default': 'config.ProductionConfig',
            'production': 'config.ProductionConfig',
            'prod': 'config.ProductionConfig'
        }.get(str(x).lower(), 'config.ProductionConfig')
	app = Flask(__name__.split('.')[0], static_folder='static', template_folder='templates', static_url_path='', instance_relative_config=True)
	app.config.from_object(get_config(get_env('FLASK_ENV', default='dev' if os.sys.platform == 'win32' else 'prod')))
	app.config.from_pyfile('config.cfg', silent=True)
	print(app.secret_key)

	# Blueprints
	register(app)

	return app, SQLAlchemy(app)

def register(app):
	from .views import blueprint
	from .utils import replace
	app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app', 'api')))

	import os
	os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
	#import importlib
	#for _mod in [_ for _ in os.listdir('.') if os.path.isdir(_) and not _.startswith('_')]:
	#	try:
	#		_lib = importlib.import_module('.'.join([__name__, _mod]))
	#	except ModuleNotFoundError:
	#		pass
	#	else:
	#		try:
	#			_lib.register(app)
	#		except AttributeError:
	#			pass
	from .utils.lib import import_from
	for _mod in [_ for _ in os.listdir('.') if os.path.isdir(_) and not _ in ['utils', 'migrations'] and not _.startswith('_')]:
		try:
			_lib = import_from('.'.join([__name__, _mod]))
		except ModuleNotFoundError:
			pass
		else:
			try:
				_lib.register(app)
			except AttributeError:
				pass

