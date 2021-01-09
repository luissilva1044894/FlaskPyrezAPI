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

from .controllers.channel_emotes import get_channel_emotes
from .controllers.random_viewer import random_viewer_func
from .controllers.uptime import uptime_func
from utils import environ
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)

twitch = create_blueprint(__name__)

'''
@twitch.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@twitch.before_app_first_request
def before_app_first_request_handler():
  twitch.base_url, twitch.client_id, twitch.oauth_token = environ.get_env('TWITCH_API_BASE_URL'), environ.get_env('TWITCH_API_CLIENT_ID'), environ.get_env('TWITCH_API_OAUTH_TOKEN')
'''

@twitch.errorhandler(ConnectionError)
@twitch.errorhandler(HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@twitch.errorhandler(404)
@twitch.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(twitch)

@twitch.route('/random_viewer', methods=['GET'])
@decorators.field_required(field=['channel', 'channel_id'])
@decorators.field_required(field='exclude', surpress_exceptions=True)
@decorators.field_required(field='ignore', surpress_exceptions=True)
def random_viewer_handler():
  #>>> import re
  #>>> re.match('([@$:{}A-z0-9]{1,50})', '@nonsocial_')
  """Retrieves a list of users that are currently logged into chat in the specified channel, then picks one of them randomly.

  Parameters
  ----------
  channel
    The channel to retrieve the logged in users from.
  exclude
    A comma-separated list of users you wish to ignore.
  ignore
    A comma-separated list of groups you wish to ignore. These groups are the specific user types. Currently that means the following: moderators, staff, admins, global_mods, viewers.
  """
  return random_viewer_func(g.channel, g.exclude, g.ignore)

@twitch.route('/channel_emotes', methods=['GET'])
@decorators.field_required(field=['channel', 'channel_id'])
def channel_emotes_handler():
  return get_channel_emotes(g.channel)

@twitch.route('/uptime', methods=['GET'])
@decorators.field_required(field=['channel', 'channel_id'])
@decorators.field_required(field='online_msg', surpress_exceptions=True)
@decorators.field_required(field='offline_msg', surpress_exceptions=True)
def uptime_handler():
  """Returns how long the specified channel has been live for the current broadcast.

  Parameters
  ----------
  channel
    The channel name.
  offline_msg
    A custom message to display when the channel is offline. - Default: :channel is currently offline.
  """
  return uptime_func(channel=g.channel, online_msg=g.online_msg, offline_msg=g.offline_msg, base_url=environ.get_env('TWITCH_API_BASE_URL'), client_id=environ.get_env('TWITCH_API_CLIENT_ID'), oauth_token=environ.get_env('TWITCH_API_OAUTH_TOKEN'))
