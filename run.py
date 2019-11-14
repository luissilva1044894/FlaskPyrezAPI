# -*- coding: utf-8 -*-

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app.utils import get_env

def create_app():
	import os

	from flask import Flask
	from flask_sqlalchemy import SQLAlchemy

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

	@app.teardown_request
	def teardown_request_func(error=None):
		"""
		This function will run after a request, regardless if an exception occurs or not.
		It's a good place to do some cleanup, such as closing any database connections.
		If an exception is raised, it will be passed to the function.
		You should so everything in your power to ensure this function does not fail, so
		liberal use of try/except blocks is recommended.
		"""
		if error:
			# Log the error
			app.logger.error(error)
	@app.route('/index', methods=['GET'])
	@app.route('/index.html', methods=['GET'])
	@app.route('/', methods=['GET'])
	def _root(error=None):
		from flask import redirect, url_for
		return redirect(url_for('api.root'))
	@app.after_request
	def jsonify_request(response):
		"""JSONify the response. https://github.com/Fuyukai/OWAPI/blob/master/owapi/app.py#L208"""
		if response.headers['Content-Type'].lower().rfind('application/json') != -1:
			from flask import request
			import json
			if request.args.get('format', 'json') in ['json_pretty', 'pretty']:
				from datetime import datetime, timedelta, timezone
				from email.utils import format_datetime
				
				response.set_data(json.dumps(response.get_json(), sort_keys=True, indent=4, separators=(',', ': ')))
				response.headers['Cache-Control'] = 'public, max-age=300'
				response.headers['Expires'] = format_datetime((datetime.utcnow() + timedelta(seconds=300)).replace(tzinfo=timezone.utc), usegmt=True)
		return response
	def get_http_exception_handler(app):
		"""Overrides the default http exception handler to return JSON."""
		from functools import wraps
		handle_http_exception = app.handle_http_exception

		@wraps(handle_http_exception)
		def ret_val(error):
			"""Generic exception handler for general exceptions"""
			if not app.env.lower().startswith('dev') and error.code == 404:
				from flask import redirect, url_for
				return redirect(url_for('api.root'))
			#from werkzeug.exceptions import HTTPException
			#if isinstance(e, HTTPException) and (500 <= e.code < 600):
			#	return error
			if not hasattr(error, 'code'):# or isinstance(error, HTTPException):
				error.code = 500
			from werkzeug.exceptions import default_exceptions
			if error.code in default_exceptions:
				# Returning directly as below results in missing Location header
				# on 301 errors which is useful for this test as it will fail to redirect.
				def get_http_error_code(error_code=500):
					return {
						301: u'Moved Permanently', 302: u'Found', 303: u'See Other', 304: u'Not Modified',
						400: u'Bad request', 401: u'Unauthorized', 403: u'Forbidden', 404: u'Resource not found', 405: u'Method not allowed',
						408: u'Request Timeout', 409: u'Conflict', 410: u'Gone', 418: u'I am a teapot', 429: u'Too many requests',
						500: u'Internal server error', 501: u'Not Implemented', 502: u'Bad Gateway', 503: u'Service unavailable', 504: u'Gateway Timeout'
					}.get(error_code, 500)
				from flask import jsonify
				if not hasattr(error, 'original_exception'):
					error.original_exception = error or None
				return jsonify(code=get_http_error_code(error.code), description=error.description, message=str(error.original_exception), error=error.code), error.code
			return handle_http_exception(error)
		return ret_val
	# Override the HTTP exception handler.
	#app.config['TRAP_HTTP_EXCEPTIONS'] = True
	app.handle_http_exception = get_http_exception_handler(app)

	from werkzeug.exceptions import default_exceptions #werkzeug import HTTP_STATUS_CODES
	for exc in default_exceptions: #exc in HTTPException.__subclasses__() | exc in HTTP_STATUS_CODES
		app.register_error_handler(exc, get_http_exception_handler(app))
	app.register_error_handler(Exception, get_http_exception_handler(app))
	#if request.path.startswith('/api/'): return jsonify_error(ex)
	#else: return ex

	import logging
	handler = logging.FileHandler('static/flask.log')#RotatingFileHandler('flask.log', maxBytes=1024 * 1024 * 100, backupCount=3)
	handler.setLevel(logging.DEBUG if app.config['DEBUG'] else logging.INFO)
	handler.setFormatter(logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] ' '%(asctime)s %(message)s \r\n'))
	app.logger.addHandler(handler)

	# Blueprints
	from app import register
	register(app)

	return app, SQLAlchemy(app)

app, db = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('debug', Server(host='127.0.0.1', port=8080, use_debugger=True))

if __name__ == '__main__':
    db.create_all()
    manager.run()
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['DEBUG'], port=int(get_env('PORT', 5000)), host='0.0.0.0')

#https://gist.github.com/rochacbruno/b1fe0ccab1a81804def887e8ed40da57
#https://gist.github.com/rochacbruno/e44c1f0f43e89093bf7ddba77ee9feef
