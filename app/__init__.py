# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, render_template, url_for, send_from_directory, escape

from .utils import replace
blueprint = Blueprint(replace(__name__, 'app.', 'api'), __name__, static_folder='static', template_folder='templates', static_url_path='')


#https://danidee10.github.io/2016/11/20/flask-by-example-8.html
#https://exploreflask.com/en/latest/blueprints.html
#https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/#internationalized-blueprint-urls
#https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/

def register(app):
	app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app', 'api')))

	from .overwatch import register as overwatch_reg
	from .paladins import register as paladins_reg
	from .twitch import register as twitch_reg
	overwatch_reg(app)
	paladins_reg(app)
	twitch_reg(app)

@blueprint.route('/random')
def randon_number_route():
	from .utils import random, get_query, try_int
	max, min, query = try_int(get_query(request.args, 'max', 100), 100), try_int(get_query(request.args, 'min', 0), 0), get_query(request.args, 'query', None)
	if query:
		_ = str(query).split(',')
		return _[random(0, len(_) - 1)]
	return str(random(min, max))

@blueprint.route('/timestamp')
def server_timestamp_route():
	"""This endpoint returns the current server and UTC time."""
	import arrow
	from flask import jsonify
	return jsonify({ 'local': arrow.now().format('DD-MMM-YYYY HH:mm:SS ZZ'), 'unix': arrow.now().timestamp, 'utc': arrow.utcnow().format('DD-MMM-YYYY HH:mm:SS ZZ') })
