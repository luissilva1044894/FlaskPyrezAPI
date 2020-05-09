#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
  g,
  jsonify,
  render_template,
  request,
)
from requests.exceptions import (
  ConnectionError,
  HTTPError,
)

from .controllers.latest_video import latest_video_func
from ..utils import (
  fix_url_for,
  get_json,
  get_query,
  replace,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.errorhandler(ConnectionError)#Internet
@blueprint.errorhandler(HTTPError)
def connection_error_handler(error=None):
  return 'Internal Error!'

@blueprint.errorhandler(404)
@blueprint.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(g._language_), blueprint.name), lang=g._language_, my_name=blueprint.name.upper())

@blueprint.route('latest_video', methods=['GET'])
def _latest_video_route_():
  return latest_video_func(get_query(request.args, 'channel_id'))
