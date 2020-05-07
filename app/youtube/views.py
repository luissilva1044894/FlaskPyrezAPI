#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
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
  get_language,
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
  print(blueprint.root_path)
  lang = get_language(request)
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(lang), blueprint.name), lang=lang, my_name=blueprint.name.upper())

@blueprint.route('latest_video', methods=['GET'])
def latest_video_handler():
  return latest_video_func(get_query(request.args, 'channel_id'))
