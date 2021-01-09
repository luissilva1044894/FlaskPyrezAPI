#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  g,
  render_template,
  request,
)

import requests

from utils.hirez import (
  #get_platform,
  patch_notes,
)
from utils.hirez.enums.platform import get_platform
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)

from .controllers.stalk import stalk_func
from .controllers.version import version_func

realm_royale = create_blueprint(__name__)

@realm_royale.errorhandler(requests.exceptions.ConnectionError)
@realm_royale.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@realm_royale.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@realm_royale.errorhandler(404)
@realm_royale.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(realm_royale)

@realm_royale.route('/patch_notes', methods=['GET'])
#@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
def _patch_notes_route_():
  """Get the latest Patch Notes"""
  #https://cms.paladinsstrike.com/wp-json/wp-api/get-posts/1?search=update
  return patch_notes.get_patch_notes(blueprint=realm_royale, lang=g.language, requested_json=g.requested_json)

@realm_royale.route('/stalk', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
def _stalk_route_():
  """Currently online status of a specified player"""
  return stalk_func()

@realm_royale.route('/version', methods=['GET'])
def _version_route_():
  """Currently status of Realm Royale Server"""
  return version_func()
