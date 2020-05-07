#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import (
  Blueprint,
  render_template,
  request,
)
import pyrez
from pyrez.api import *
from pyrez.enumerations import (
  Champions,
  Tier,
)
from pyrez.exceptions import (
  MatchException,
  PlayerNotFound,
)
from sqlalchemy.exc import (
  IntegrityError,
  InternalError,
  OperationalError,
  ProgrammingError,
)

from ..utils import (
  fix_url_for,
  get_env,
  get_json,
  get_language,
  getPlatform,
  getPlayerName,
  LanguagesSupported,
  PlatformsSupported,
)
from .controllers.patch_notes import patch_notes_func
blueprint = Blueprint('paladins', __name__, static_folder='static', template_folder='templates', static_url_path='')

#paladinsAPI = PaladinsAPI(devId=get_env('PYREZ_AUTH_ID'), authKey=get_env('PYREZ_DEV_ID'), sessionId=lastSession.sessionId if lastSession else None)
#paladinsAPI.onSessionCreated += sessionCreated

#https://flask.palletsprojects.com/en/1.1.x/api/?highlight=flash#flask.Flask.route
#https://github.com/Kamilahsantos/Flask--Crud
#https://imasters.com.br/desenvolvimento/conhecendo-o-jinja2-um-mecanismo-para-templates-no-flasks

#from requests.exceptions import ConnectionError
#@app.errorhandler(ConnectionError)
#@app.errorhandler(Exception)

@blueprint.errorhandler(404)
@blueprint.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  lang = get_language(request)
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(lang), blueprint.name), lang=lang, my_name=blueprint.name.upper())

@blueprint.errorhandler(MatchException)
@blueprint.errorhandler(PlayerNotFound)
def player_not_found_error(error=None):
  return PLAYER_NOT_FOUND_STRINGS[language].format(player_name)

@blueprint.route('/decks', methods=['GET'])
def decks_handler():
  return '?'
@blueprint.route('/version', methods=['GET'])
def version_handler():
  return '?'
@blueprint.route('/stalk', methods=['GET'])
def stalk_handler():
  return '?'
@blueprint.route('/last_match', methods=['GET'])
def last_match_handler():
  return '?'
@blueprint.route('/live_match', methods=['GET'])
def live_match_handler():
  return '?'
@blueprint.route('/patch_notes', methods=['GET'])
def patch_notes_handler():
  return patch_notes_func()
@blueprint.route('/rank', methods=['GET'])
def rank_handler():
  return '?'
@blueprint.route('/kda', methods=['GET'])
def kda_handler():
  return '?'
