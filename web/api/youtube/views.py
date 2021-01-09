#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  g,
  render_template,
  request,
)
from requests.exceptions import (
  ConnectionError,
  HTTPError,
)

from .controllers.latest_video import latest_video_func
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)

youtube = create_blueprint(__name__)

@youtube.errorhandler(ConnectionError)
@youtube.errorhandler(HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@youtube.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  #'You need to specify a "user" (/user/ URLs) or an "id" (/channel/ URLs).'
  return f'🚫 ERROR: {error}'

@youtube.errorhandler(404)
@youtube.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(youtube)

@youtube.route('/latest_video', methods=['GET'], strict_slashes=True)
@decorators.field_required(field=['channel_id', 'channel', 'id'])
def latest_video_handler():
  """Retrieves the latest video uploaded to the specified channel and returns the title + URL for it.

  Parameters
  ----------
  channel_id
    For users with URLs that are formatted like: youtube.com/channel/[ID_HERE].
  user
    For users with URLs that are formatted like: youtube.com/user/[USERNAME_HERE].
  """
  return latest_video_func(g.channel_id)
