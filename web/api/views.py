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
	#https://gist.github.com/cybertoast/6499708
	'''Self-documenting:
		Get a list of all routes, and their endpoint's docstrings as a helper resource for API documentation. '''
	from flask import jsonify, url_for, request, current_app as app
	from utils.flask import requested_json
	import urllib
	if not requested_json(request): return get_page()
	def has_no_empty_params(rule):
		return len(rule.defaults or ()) >= len(rule.arguments or ())
	def get_doc(rule):
		if hasattr(app.view_functions[rule.endpoint], 'import_name'):
			return {rule.rule: '%s\n%s' % (','.join(list(rule.methods)), import_string(app.view_functions[rule.endpoint].import_name).__doc__)}
		return app.view_functions[rule.endpoint].__doc__ #{rule.rule: app.view_functions[rule.endpoint].__doc__}
		#.__name__ | .__module__
	#for name, func in app.view_functions.items():
	#	print(name, func)
	#	input()
	return jsonify({
		'namespace': blueprint.name.split('.')[0],
		'routes': { #'{}{}'.format(rule, '/'.join(rule.arguments)): {'endpoint': rule.endpoint, 'methods': sorted(rule.methods), 'strict_slashes': rule.strict_slashes} for rule in app.url_map.iter_rules() if 'GET' in rule.methods and has_no_empty_params(rule) and str(rule).startswith('/api')
			url_for(r.endpoint, **dict('[{}]'.format(_) for _ in r.arguments)): {
			#'endpoint': r.endpoint,
			#'line': urllib.parse.unquote('{:50s} {:20s} {}'.format(r.endpoint, ','.join(r.methods), url_for(r.endpoint, **dict('[{}]'.format(_) for _ in r.arguments)))),
			'methods': ', '.join(sorted(r.methods)), #'methods': sorted(r.methods)
			'description': get_doc(r),
			'slashes': r.strict_slashes} for r in app.url_map.iter_rules() if 'GET' in r.methods and has_no_empty_params(r) and 'api' in r.rule#str(r).startswith('/api')
		},
		'_links': {'up': [request.base_url[:request.base_url.rfind(blueprint.name.split('.')[0])]]}
	})
	'''
	routes = {'namespace': blueprint.name, 'routes': {}, '_links': {"up": [request.base_url]}}
	#rule.defaults | rule.alias
	for rule in app.url_map.iter_rules():
		if 'GET' in rule.methods and has_no_empty_params(rule) and rule.rule.startswith('/api'):
			routes['routes']['{}{}'.format(rule, '/'.join(rule.arguments))] = {'endpoint': rule.endpoint, 'methods': sorted(rule.methods), 'strict_slashes': rule.strict_slashes}
	'''
@blueprint.route('/random/')
def random_handler():
	from flask import request
	from utils import random
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
