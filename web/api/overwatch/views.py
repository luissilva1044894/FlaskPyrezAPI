#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boolify import boolify
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
from utils import environ
from utils.hirez.enums.platform import get_platform
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)
def fix_bool(b):
  return boolify(b)

def fix_link(env, lang):
  def fix_plat(lang):
    if hasattr(lang, 'lang_code'):
      lang = lang.lang_code
    return str(lang).lower().replace('_', '-').replace('la', 'es')
  return env.format(lang=fix_plat(lang))

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
  """Get the latest Patch Notes"""
  return patch_notes.patch_notes_func(fix_link(environ.get_env('OVERWATCH_WEBSITE'), g.language), environ.get_env('OVERWATCH_PATCH_NOTES_CLASS_NAME') or 'PatchNotes-patch')

@overwatch.route('/rank', methods=['GET'])
@decorators.field_required(field=['player', 'player_id', 'player_name'])
@decorators.field_required(field=['platform', 'plat'], surpress_exceptions=True, call_method=get_platform)
@decorators.field_required(field='average_sr', surpress_exceptions=True, call_method=fix_bool)
@decorators.field_required(field='wr', surpress_exceptions=True, call_method=fix_bool)
def rank_handler():
  """Currently rank of a specified player"""
  # http://127.0.0.1:5000/api/overwatch/rank?player=nonsocial
  # 🚫 ERROR: An unexpected error has occurred! 404 Client Error: Not Found for url: https://ow-api.com/v1/stats/None/us/nonsocial/profile
  print(g.__dict__)
  return rank.rank_func(battle_net=g.player, platform=g.platform, lang=g.language, paladins_like=g.wr, format_average_sr=g.average_sr)
