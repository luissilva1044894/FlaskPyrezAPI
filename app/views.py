#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
	abort,
	Blueprint,
  g,
	jsonify,
	render_template,
	request,
)
from arrow import (
  now,
  utcnow,
)
from .utils import (
  fix_url_for,
  get_json,
  get_query,
  replace,
)
from .utils.num import (
  random_func,
  try_int,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api').replace('views', ''), __name__, static_folder='static', template_folder='templates', static_url_path='')

#https://danidee10.github.io/2016/11/20/flask-by-example-8.html
#https://exploreflask.com/en/latest/blueprints.html
#https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/#internationalized-blueprint-urls
#https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@blueprint.route('/', methods=['GET'])
def root():
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(g._language_), blueprint.name), lang=g._language_, my_name=blueprint.name.upper())

@blueprint.route('/random')
def random_number_route():
  max, min, query = try_int(get_query(request.args, 'max', 100), 100), try_int(get_query(request.args, 'min', 0), 0), get_query(request.args, 'query', None)
  if query:
    _ = str(query).split(',')
    return _[random_func(0, len(_) - 1)]
  return str(random_func(min, max))

@blueprint.route('/timestamp')
def server_timestamp_route():
  """This endpoint returns the current server and UTC time."""
  return jsonify({ 'local': now().format('DD-MMM-YYYY HH:mm:SS ZZ'), 'unix': now().timestamp, 'utc': utcnow().format('DD-MMM-YYYY HH:mm:SS ZZ') })
