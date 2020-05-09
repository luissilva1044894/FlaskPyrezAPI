#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
  g,
  render_template,
  request,
)

from .controllers import random_viewer_function
from ..utils import (
  fix_url_for,
  get_json,
  get_query,
  replace,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.errorhandler(404)
@blueprint.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(g._language_), blueprint.name), lang=g._language_, my_name=blueprint.name.upper())

@blueprint.route('/random_viewer', methods=['GET'])
def _random_viewer_route_():
  return random_viewer_function(get_query(request.args, 'channel'), str(get_query(request.args, 'exclude')).split(','), get_query(request.args, 'ignore'))
