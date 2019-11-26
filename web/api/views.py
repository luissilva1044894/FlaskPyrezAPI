#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint, is_async
from utils import get_env

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', url_prefix='/{}'.format('/'.join(__blueprint__name[:-1])))

def get_page():
	if is_async():
		from quart import request
	else:
		from flask import request
	return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
	#https://gist.github.com/cybertoast/6499708
	'''Self-documenting: Get a list of all routes, and their endpoint's docstrings as a helper resource for API documentation. '''
	if is_async():
		from quart import jsonify, url_for, request, current_app as app
	else:
		from flask import jsonify, url_for, request, current_app as app
	from utils.web import requested_json
	import urllib
	if not requested_json(request): return get_page()
	def has_no_empty_params(rule):
		if hasattr(rule, 'arguments'):
			return len(rule.defaults or ()) >= len(rule.arguments or ())
		return True
	def get_doc(rule):
		if hasattr(app.view_functions[rule.endpoint], 'import_name'):
			return {rule.rule: '%s\n%s' % (','.join(list(rule.methods)), import_string(app.view_functions[rule.endpoint].import_name).__doc__)}
		return app.view_functions[rule.endpoint].__doc__ #{rule.rule: app.view_functions[rule.endpoint].__doc__}
		#.__name__ | .__module__
	#for name, func in app.view_functions.items():
	#	print(name, func)
	#	input()
	def url_for_rule(r):
		if hasattr(r, 'arguments'):
			return url_for(r.endpoint, **dict('[{}]'.format(_) for _ in r.arguments))
		return url_for(r.endpoint)
	#for r in app.url_map.iter_rules(): print(r.rule)
	return jsonify({
		'namespace': blueprint.name.split('.')[0],
		'routes': { #'{}{}'.format(rule, '/'.join(rule.arguments)): {'endpoint': rule.endpoint, 'methods': sorted(rule.methods), 'strict_slashes': rule.strict_slashes} for rule in app.url_map.iter_rules() if 'GET' in rule.methods and has_no_empty_params(rule) and str(rule).startswith('/api')
			url_for_rule(r): {
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
	from utils import random
	from utils.web import get
	from utils.num import try_int
	_max, _min = try_int(get('max'), 100), try_int('min')
	return str(random(_min, _max, args=[_ for _ in get('query', '').split(',') if _]))

@blueprint.route('/timestamp/')
def server_timestamp_handler():
	"""This endpoint returns the current server and UTC time."""
	from arrow import now, utcnow
	if is_async():
		from quart import jsonify
	else:
		from flask import jsonify
	return jsonify({ 'local': now().format('DD-MMM-YYYY HH:mm:SS ZZ'), 'unix': now().timestamp, 'utc': utcnow().format('DD-MMM-YYYY HH:mm:SS ZZ') })
