#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  g,
  request,
)

#from .controllers.rank import rank_func
#from .controllers.patch_notes import patch_notes_func

from requests.exceptions import (
  ConnectionError,
  HTTPError,
)

from .controllers.random_viewer import random_viewer_func
from utils import web

twitch = web.create_blueprint(__name__)

'''
@twitch.errorhandler(web.exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'
'''

@twitch.errorhandler(ConnectionError)
@twitch.errorhandler(HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@twitch.errorhandler(404)
@twitch.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return web.get_page(twitch)

@twitch.route('/random_viewer', methods=['GET'])
@web.decorators.field_required(field=['channel', 'channel_id'])
@web.decorators.field_required(field='exclude', surpress_exceptions=True)
@web.decorators.field_required(field='ignore', surpress_exceptions=True)
def random_viewer_handler():
  return random_viewer_func(g.channel, g.exclude, g.ignore)
