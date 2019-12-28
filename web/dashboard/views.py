#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint, decorators, is_async

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', template_folder='templates', url_prefix='/{}'.format('/'.join(__blueprint__name[:-1])))

from functools import wraps
if is_async():
	from quart import g, request, redirect, url_for, render_template, session, abort
else:
	from flask import g, request, redirect, url_for, render_template, session, abort

def auth(x):
	#return request.cookies.get('logged_in', None)
	return 'logged_in' in session

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		print(request.url[request.url.rfind('://')+ 3:].split('/', 1)[0])
		#input(dir(request))
		if auth(request):
			return f(*args, **kwargs)
		# if user is not logged in, redirect to login page
		return redirect(url_for('.secret_page', redirect_to=request.url))
	return decorated_function
#https://scotch.io/tutorials/authentication-and-authorization-with-flask-login
#https://pythonspot.com/login-authentication-with-flask/
#https://flask-caching.readthedocs.io/en/latest/
#https://pythonise.com/series/learning-flask/custom-flask-decorators
#@blueprint.before_request
#def do_before_request():
	#	g.user = get_user_from_session()
#https://github.com/cookiecutter-flask/cookiecutter-flask/tree/master/%7B%7Bcookiecutter.app_name%7D%7D
#https://github.com/mjhea0/flask-basic-registration/blob/master/project/__init__.py
#https://github.com/JackStouffer/Flask-Foundation/blob/master/appname/controllers/main.py
@blueprint.route('/', methods=['GET'])
@decorators.templated('index.html')
@login_required
def home():
	return dict(title='HOME')
	#return render_template('index.html')
#https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
#<input type="hidden" value="{{ request.args.get('redirect_to', '') }}"/>
@blueprint.route('/login', methods=['GET', 'POST'])
@decorators.templated('login.html')
def secret_page():
	if request.method == 'POST':
		from utils import get_env
		if not hasattr(g, '__cookies__'):
			g.__cookies__ = []
		g.__cookies__.append({'name': 'logged_in'})
		if not request.form.get('form-token', '') == get_env('DISCORD_BOT_TOKEN'):
			abort(403)
		from boolify import boolify
		#if boolify(request.form.get('form-remember')):
		session['logged_in'] = True
		return redirect(request.args.get('redirect_to', url_for('.home')))#return_to
	return dict(title='Login')
'''
@blueprint.route('/<short_url>', methods=['GET'])
def redirect_short_url(short_url):
	from flask import redirect, url_for
	import base64
	p = Post.query.filter_by(id=to_base_10(short_url)).first() # converting into decimal format
	if p:
		print(base64.urlsafe_b64decode(p.url))
		redirect(base64.urlsafe_b64decode(p.url))
	return redirect(url_for('.home_get'))# fallback if no URL is found
'''
#https://www.encode.io/httpx/async/