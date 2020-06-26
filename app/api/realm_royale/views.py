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

from utils.web import (
  auto_doc,
  create_blueprint,
  decorators,
  exceptions,
  get_page,
  requested_json,
)

from .controllers.patch_notes import patch_notes_func
from .controllers.stalk import stalk_func
from .controllers.version import version_func

realm_royale = create_blueprint(__name__)

@realm_royale.errorhandler(ConnectionError)
@realm_royale.errorhandler(HTTPError)
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
def _patch_notes_route_():
  return patch_notes_func()

@realm_royale.route('/stalk', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
def _stalk_route_():
  """Currently online status of a specified player"""
  return stalk_func()

@realm_royale.route('/version', methods=['GET'])
def _version_route_():
  """Currently status of Realm Royale Server"""
  return version_func()
