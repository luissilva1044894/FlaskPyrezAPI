#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from utils import replace

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def get_page():
	from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	"""Homepage route."""
	return get_page()

@blueprint.route('/random/')
def random_handler():
	from utils import get, random
	from utils.flask import get
	from utils.num import try_int
	_max, _min = try_int(get('max'), 100), try_int('min')
	return str(random(_min, _max, args=[_ for _ in get('query', '').split(',') if _]))

@blueprint.route('/timestamp/')
def server_timestamp_handler():
	"""This endpoint returns the current server and UTC time."""
	from arrow import now, utcnow
	from flask import jsonify
	return jsonify({ 'local': now().format('DD-MMM-YYYY HH:mm:SS ZZ'), 'unix': now().timestamp, 'utc': utcnow().format('DD-MMM-YYYY HH:mm:SS ZZ') })
