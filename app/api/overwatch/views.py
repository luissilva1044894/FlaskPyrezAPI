#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  g,
  request,
)
from requests.exceptions import (
  ConnectionError,
  HTTPError,
)

from .controllers import (
  rank,
  patch_notes,
)
from utils.web import (
  create_blueprint,
  decorators,
  exceptions,
  get_page,
  get_value,
)

overwatch = create_blueprint(__name__)

@overwatch.errorhandler(ConnectionError)
@overwatch.errorhandler(HTTPError)
def connection_error_handler(error=None):
  #print(error, error.__dict__, error.request.__dict__)
  return f'🚫 ERROR: An unexpected error has occurred!\r\n{error}'

@overwatch.errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  return f'🚫 ERROR: {error}'

@overwatch.errorhandler(404)
@overwatch.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(overwatch)

@overwatch.route('/patch_notes', methods=['GET'])
def patch_notes_handler():
  return patch_notes.patch_notes_func()

@overwatch.route('/rank', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field='platform', surpress_exceptions=True)
def rank_handler():
  """Currently rank of a specified player"""
  return rank.rank_func(get_value('player'), get_value('platform'))
