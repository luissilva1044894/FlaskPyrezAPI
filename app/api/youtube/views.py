#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  Blueprint,
  g,
  render_template,
  request,
)
from requests.exceptions import (
  ConnectionError,
  HTTPError,
)

from .controllers.latest_video import latest_video_func
from utils.web import (
  create_blueprint,
  exceptions,
  get_page,
)
from utils.web.decorators import field_required

youtube = create_blueprint(__name__)

@youtube.errorhandler(ConnectionError)
@youtube.errorhandler(HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@youtube.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@youtube.errorhandler(404)
@youtube.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(youtube)

@youtube.route('/latest_video', methods=['GET'], strict_slashes=True)
@field_required(field=['channel_id', 'channel', 'id'])
def latest_video_handler():
  return latest_video_func(g.channel_id)
