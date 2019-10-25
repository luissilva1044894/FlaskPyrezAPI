#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError

from decouple import config
import os

import pyrez
from pyrez.api import *
from pyrez.exceptions import PlayerNotFound, MatchException
from pyrez.enumerations import Champions, Tier

from ..utils import getPlatform, getPlayerName, PlatformsSupported, LanguagesSupported

blueprint = Blueprint('paladins', __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.route('/testando', methods=['GET'])
def testando():
	return "DONE"

PYREZ_AUTH_ID = os.getenv('PYREZ_AUTH_ID', config('PYREZ_AUTH_ID'))
PYREZ_DEV_ID = os.getenv('PYREZ_DEV_ID', config('PYREZ_DEV_ID'))
#print(PYREZ_DEV_ID, PYREZ_AUTH_ID)
#paladinsAPI = PaladinsAPI(devId=PYREZ_DEV_ID, authKey=PYREZ_AUTH_ID, sessionId=lastSession.sessionId if lastSession else None)
#paladinsAPI.onSessionCreated += sessionCreated

@blueprint.route('/decks', methods=['GET'])
@blueprint.route('/deck', methods=['GET'])
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
@blueprint.route('/kda', methods=['GET'])
@blueprint.route('/winrate', methods=['GET'])
def getWinrate():
    return '?'
