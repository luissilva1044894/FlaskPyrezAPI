#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import requests

from .controllers.kda import kda_func
from .controllers.live_match import live_match_func
from .controllers.patch_notes import patch_notes_func
from .controllers.rank import rank_func
from .controllers.stalk import stalk_func
from .controllers.version import version_func

from utils import web

smite = web.create_blueprint(__name__)

@smite.errorhandler(requests.exceptions.ConnectionError)
@smite.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@smite.errorhandler(web.exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@smite.errorhandler(404)
@smite.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return web.get_page(smite)

@smite.route('/kda', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
@web.decorators.field_required(field=['god', 'god_id', 'god_name'], surpress_exceptions=True)
def _kda_route_():
  """KDA of a player or champion"""
  return flask.g.__dict__#kda_func()

@smite.route('/last_match', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _last_match_route_():
  """Get information about a previously finished match"""
  return 'last_match route'

@smite.route('/live_match', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _live_match_route_():
  """All players rank in a live match"""
  return live_match_func('a', 'b')

@smite.route('/patch_notes', methods=['GET'])
def _patch_notes_route_():
  return patch_notes_func()

@smite.route('/rank', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _rank_route_():
  """Currently rank of a specified player"""
  return rank_func('a', 'b')

@smite.route('/stalk', methods=['GET'])
@web.decorators.field_required(field=['player', 'player_id', 'player_name'])
def _stalk_route_():
  """Currently online status of a specified player"""
  return stalk_func()

@smite.route('/version', methods=['GET'])
def _version_route_():
  """Currently status of Smite Server"""
  return version_func()
