#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
  jsonify,
  request,
)
from requests.exceptions import (
  ConnectionError,
  HTTPError,
)

from .controllers.latest_video import latest_video_func
from ..utils import (
  get_query,
  replace,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.errorhandler(ConnectionError)#Internet
@blueprint.errorhandler(HTTPError)
def connection_error_handler(error=None):
  return 'Internal Error!'

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
  """Homepage route."""
  return 'Homepage'

@blueprint.route('latest_video', methods=['GET'])
def latest_video_handler():
  return latest_video_func(get_query(request.args, 'channel_id'))
