#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError

from decouple import config
import os

import pyrez
from pyrez.api import *
from pyrez.enumerations import Champions, Tier

from ..utils import getPlatform, getPlayerName, PlatformsSupported, LanguagesSupported

blueprint = Blueprint('paladins', __name__, static_folder='static', template_folder='templates', static_url_path='')

PYREZ_AUTH_ID = os.getenv('PYREZ_AUTH_ID', config('PYREZ_AUTH_ID'))
PYREZ_DEV_ID = os.getenv('PYREZ_DEV_ID', config('PYREZ_DEV_ID'))
#print(PYREZ_DEV_ID, PYREZ_AUTH_ID)
#paladinsAPI = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, sessionId=lastSession.sessionId if lastSession else None)
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
    from app.utils import fix_url_for, get_json
    return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json('pt'), blueprint.name), lang='pt', my_name=blueprint.name.upper())

from pyrez.exceptions import MatchException, PlayerNotFound
@blueprint.errorhandler(MatchException)
@blueprint.errorhandler(PlayerNotFound)
def player_not_found_error(error=None):
	return PLAYER_NOT_FOUND_STRINGS[language].format(playerName)

@blueprint.route('/deck', methods=['GET'])
@blueprint.route('/decks', methods=['GET'])
def getDecks():
    return '?'
@blueprint.route('/version', methods=['GET'])
def getGameVersion():
    return '?'
@blueprint.route('/stalk', methods=['GET'])
def getStalk():
    return '?'
@blueprint.route('/lastmatch', methods=['GET'])
def getLastMatch():
    return '?'
@blueprint.route('/currentmatch', methods=['GET'])
def getCurrentMatch():
    return '?'
@blueprint.route('/rank', methods=['GET'])
def getRank():
    return '?'
@blueprint.route('/winrate', methods=['GET'])
@blueprint.route('/kda', methods=['GET'])
def getWinrate():
    return '?'
