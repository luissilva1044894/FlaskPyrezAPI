#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask

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
def register_blueprints(app, _root=None, *, recursive=True, include_packages=False):
	"""Automagically register all blueprint packages. Just take a look in the blueprints directory."""
	from os import listdir, getcwd
	from os.path import isfile, join, isdir
	from werkzeug.utils import find_modules, import_string
	import importlib
	import os
	for _ in [ _ for _ in listdir('.') if not _[0]=='_' and not _[0]=='.']:
		for path, subdirs, files in os.walk(_):
			for __ in [ _[:-3] for _ in files if not _[0]=='_' and not _[0]=='.' and _[-3:]=='.py']:
				try:
					mod = importlib.import_module(os.path.join(path, __).replace('\\', '.').replace('/', '.'))
				except (ModuleNotFoundError, ImportError, AttributeError) as exc:
					print(f'>>> Failed to load: {exc}')
					pass
				else:
					if hasattr(mod, 'blueprint'):
						app.register_blueprint(mod.blueprint)
						print(f'>>> Loaded blueprint: {mod.blueprint.name}', '|', mod.__name__.split('.')[-2], f'({mod.__name__})')
def load_config(app, _env_name='FLASK_ENV', _config_filename='config.cfg'):
	from utils import get_env
	from utils.web import get_config
	import os

	# Config from object
	app.config.from_object(get_config(get_env(_env_name, default='dev' if os.sys.platform == 'win32' or os.name == 'nt' else 'prod')))
	app.config.from_pyfile(_config_filename, silent=True)
	#app.config.from_envvar('APP_CONFIG') # Config from filepath in env

def register_jsonify(app):
	from utils.web import is_async
	if is_async():
		@app.after_request
		async def jsonify_func(response):
			from utils.web import ajsonify
			return await ajsonify(app, response)
	else:
		@app.after_request
		def jsonify_func(response):
			"""JSONify the response. https://github.com/Fuyukai/OWAPI/blob/master/owapi/app.py#L208"""
			#if flask.request.headers.get('Content-Type', '').lower() == 'application/json': print(flask.request.get_data().decode('utf-8'))#request.data
			from utils.web import jsonify
			return jsonify(app, response)
def register_teardowns(app):
	@app.teardown_appcontext
	#@app.teardown_request
	def teardown_request_func(error=None):
		"""Log the error"""
		if error:
			app.logger.error(error)

def get_path(path, folder, _dir='data'):
	import os
	return os.path.join(path, _dir, folder)
def check_redirects(app):
	#@app.before_request
	@app.before_first_request
	def do_before_request():
		if isinstance(app, flask.Flask):
			from flask import request, g
		else:
			from quart import request, g
		scheme = request.headers.get('X-Forwarded-Proto')
		# https://stackoverflow.com/questions/32237379/python-flask-redirect-to-https-from-http/50041843
		# if not request.is_secure and app.env != 'development':
		if scheme and scheme == 'http' and request.url.startswith('http://'):
			return redirect(request.url.replace('http://', 'https://', 1), code=301)
		g.__cookies__ = []
		from utils.file import read_file
		for _ in (read_file('data/redirects.json', is_json=True) or {}).get('redirect', {}):
			if _.get('path') and _.get('path').lower() == request.path.lower():
				if isinstance(app, flask.Flask):
					from flask import redirect, url_for
				else:
					from quart import redirect, url_for
				return redirect(url_for(_.get('for')))
		'''#redirect_old
		for _ in __kwargs__:
			for __ in __kwargs__[_]:
				if request.path == __: #request.full_path
					from flask import redirect, url_for
					_split = __.split('/')[1:]
					return redirect(url_for(f'{_split[0]}.{_}.views.{_split[1]}_handler'))
		'''
def check_db(app):
	@app.before_request
	def do_before_request():
		from .models import db
		from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
		try:
			from .models.paladins.player import Player
			if not Player.query.all():
				pass #new_user = Player(id=123, name='Nonsocial', platform='PC')#session = Session('alsalsajkas')
		except (IntegrityError, InternalError, OperationalError, ProgrammingError) as exc:
			try:
				print('>>> Creating Database')
				db.drop_all()
				db.create_all()
			except Exception as exc:
				print(exc)
		else:
			for _ in Player.query.all():
				print(_)
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
def create_manager(app):
	from flask_script import Manager, Server, Shell #flask.ext.script
	from flask_migrate import Migrate, MigrateCommand

	from utils import get_env
	from .models import db
	from boolify import boolify

	migrate = Migrate(app=app, db=db)
	manager = Manager(app=app)

	@manager.command
	def update_db():
		from .models.paladins.champ import Champ
		print('>>> Initializing...')
		try:
			Champ.query.first()
		except:
			reset_db()
		finally:
			import pyrez
			from utils import get_env
			Champ.update(pyrez.PaladinsAPI(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID')))
		print('>>> Database updated!')
		import sys
		sys.exit(0)

	_debug_mod = boolify(get_env('DEBUG')) or not 'heroku' in get_env('PYTHONHOME', '').lower()

	@manager.command
	def list_routes():
		from urllib.parse import unquote
		[print(_) for _ in sorted(unquote('{:50s} {:20s} {}'.format(r.endpoint, ','.join(r.methods), r)) for r in app.url_map.iter_rules())]
	@manager.command
	def create_db():
		db.create_all()
	@manager.command
	def drop_db():
		db.drop_all()
	@manager.command
	def reset_db():
		drop_db()
		create_db()
	@manager.command
	def schedule_task():
		t = 'i am a scheduled action, yeah'
		print(t)
		app.logger.debug(t)
	def make_shell_context():
		return dict(app=app, db=db)
	if _debug_mod:
		@app.route('/debug/')
		def _debug():
			"""deliberate error, test debug working"""
			assert False, 'oops'
	#@manager.command
	#def my_function():
	#	x = app.url_map
	#	print("hi")

	manager.add_command('db', MigrateCommand)
	manager.add_command('debug', Server(host=get_env('HOST', default='0.0.0.0'), port=get_env('PORT', default=5000), use_debugger=_debug_mod))
	manager.add_command('shell', Shell(make_context=make_shell_context))

	return manager

from utils.web import decorators
@decorators.auto_register_blueprints(attr='blueprint', meth='register_blueprint')
def create_app(app_name=None, *, is_async=False, static_folder=None, template_folder=None, static_url_path=None, instance_relative_config=True):
	app_name = app_name or __name__.split('.')[0]
	root_path = __file__[:__file__.rfind(app_name)]
	import os
	if is_async or os.environ.get('SERVER_MODE'):
		from quart import Quart
		app = Quart(app_name, static_folder=static_folder or get_path(root_path, 'static'), template_folder=template_folder or get_path(root_path, 'templates'), static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)
		os.environ.update({'SERVER_MODE': 'SERVER_MODE'})
	else:
		app = flask.Flask(app_name, static_folder=static_folder or get_path(root_path, 'static'), template_folder=template_folder or get_path(root_path, 'templates'), static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)
		os.environ.pop('SERVER_MODE', None)
		#app = Flask(app_name, static_folder=static_folder or 'static', template_folder=template_folder or g'templates', static_url_path=static_url_path or '', instance_relative_config=instance_relative_config)
	load_config(app)
	#configure_logging(app)
	#configure_extensions(app)
	if is_async:
		pass
	initialize_plugins(app)
	'''
	with app.app_context():
		## Initialize Plugins
		initialize_plugins(app)
		#register_blueprints(app, app.name)
		#register_context_processor(app)
		register_jsonify(app)
		check_db(app)
		check_redirects(app)
	'''
	#initialize_plugins(app)
	register_jsonify(app)
	#check_db(app)
	check_redirects(app)
	return app

#The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.

#https://philipwalton.github.io/solved-by-flexbox/demos/input-add-ons/
#https://www.maujor.com/tutorial/anti-heroi-css-display-table.php#header
