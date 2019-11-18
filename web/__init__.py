#!/usr/bin/env python
# -*- coding: utf-8 -*-

def configure_logging(app=None):
	"""Register root logging"""
	import logging
	if not app:
		logging.basicConfig(level=logging.DEBUG)
		logging.getLogger('werkzeug').setLevel(logging.INFO)
	else:
		import os
		logs_folder = os.path.join(app.static_folder, app.config['LOG_PATH'])
		from utils.file import create_folder
		create_folder(logs_folder)
		if not app.config.get('TESTING', None):
			if not app.config['DEBUG']:
				handler = logging.FileHandler(os.path.join(logs_folder, app.config['LOG_FILENAME']))#RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=3)
				handler.setLevel(logging.DEBUG)#logging.INFO
				handler.setFormatter(logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] ' '%(asctime)s %(message)s \r\n'))
				app.logger.addHandler(handler)
def register_blueprints(app, _root=None, recursive=True, include_packages=False):
	"""Automagically register all blueprint packages. Just take a look in the blueprints directory."""
	from os import listdir, getcwd
	from os.path import isfile, join, isdir
	from werkzeug.utils import find_modules, import_string
	import importlib
	import os
	for _ in [ _ for _ in listdir('.') if not _.startswith('_') and not _.startswith('.')]:
		for path, subdirs, files in os.walk(_):
			for __ in [ _[:-3] for _ in files if not _.startswith('_') and not _.startswith('.') and _.endswith('.py')]:
				try:
					mod = importlib.import_module(os.path.join(path, __).replace('\\', '.').replace('/', '.'))
				except (ModuleNotFoundError, ImportError, AttributeError) as exc:
					pass
				else:
					if hasattr(mod, 'blueprint'):
						app.register_blueprint(mod.blueprint)
						#print(f'>>> Loaded blueprint: {mod.blueprint.name}')
						print('>>> Loaded blueprint: {} | {} ({})'.format(mod.blueprint.name, mod.__name__.split('.')[-2], mod.__name__))
def load_config(app, _env_name='FLASK_ENV', _config_filename='config.cfg'):
	from utils import get_env
	from utils.flask import get_config
	import os

	# Config from object
	app.config.from_object(get_config(get_env(_env_name, default='dev' if os.sys.platform == 'win32' or os.name == 'nt' else 'prod')))
	app.config.from_pyfile(_config_filename, silent=True)
	#app.config.from_envvar('APP_CONFIG') # Config from filepath in env

def register_jsonify(app):
	@app.after_request
	def jsonify_func(response):
		"""JSONify the response. https://github.com/Fuyukai/OWAPI/blob/master/owapi/app.py#L208"""
		#if flask.request.headers.get('Content-Type', '').lower() == 'application/json': print(flask.request.get_data().decode('utf-8'))#request.data
		if response.headers.get('Content-Type', '').lower() == app.config['JSONIFY_MIMETYPE'].lower():
			from flask import request
			if request.args.get('format', 'json') in ['json_pretty', 'pretty'] or app.config['JSONIFY_PRETTYPRINT_REGULAR']:
				import json
				from datetime import datetime, timedelta, timezone
				from email.utils import format_datetime
				response.set_data(json.dumps(response.get_json(), sort_keys=app.config['JSON_SORT_KEYS'], ensure_ascii=app.config['JSON_AS_ASCII'], indent=4, separators=(',', ': ')))
				response.headers['Cache-Control'] = 'public, max-age=300'
				response.headers['Expires'] = format_datetime((datetime.utcnow() + timedelta(seconds=300)).replace(tzinfo=timezone.utc), usegmt=True)
		return response
def register_teardowns(app):
	@app.teardown_appcontext
	#@app.teardown_request
	def teardown_request_func(error=None):
		if error:
			# Log the error
			app.logger.error(error)

def get_path(path, folder, _dir='data'):
	import os
	#input(os.path.isdir(get_path(root_path, 'static')))
	return os.path.join(path, _dir, folder)

def initialize_plugins(app):
	from .models import db
	db.init_app(app)

	#import os
	# Build a sample db on the fly, if one does not exist yet.
	#database_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), f'{__name__}.sqlite')#app.config['DATABASE_FILE'])
	#if not os.path.exists(database_path):
	#	from .models import db
		#db.drop_all()
		#db.create_all()
	try:
		from .models import Paladins
		from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
		#input(getattr(Paladins, 'query').all())

		if not Paladins.query.all():
			pass
			#new_user = Paladins(id=123, name='Nonsocial', platform='PC')
			#session = Session('alsalsajkas')
	except (IntegrityError, InternalError, OperationalError, ProgrammingError) as exc:
		print('>>> Creating Database')
		try:
			db.drop_all()
			db.create_all()
		except Exception as exc:
			print(exc)
	else:
		for _ in Paladins.query.all():
			print(_)
	
def create_app(app_name=None, *, static_folder=None, template_folder=None, static_url_path=None, instance_relative_config=True):
	from flask import Flask
	app_name = app_name or __name__.split('.')[0]
	root_path = __file__[:__file__.rfind(app_name)]
	app = Flask(app_name, static_folder=static_folder or get_path(root_path, 'static'), template_folder=template_folder or get_path(root_path, 'templates'), static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)
	#app = Flask(app_name, static_folder=static_folder or 'static', template_folder=template_folder or g'templates', static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)
	load_config(app)
	#configure_logging(app)
	#configure_extensions(app)
	with app.app_context():
		## Initialize Plugins
		initialize_plugins(app)
		register_blueprints(app, app.name)
		#regiter_context_processor(app)
		register_jsonify(app)
	return app

#The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
