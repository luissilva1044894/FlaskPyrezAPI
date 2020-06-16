#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from datetime import datetime
import json
import os

from flask import (
  abort,
  escape,
  Flask,
  g,
  jsonify,
  render_template,
  request,
  send_from_directory,
  url_for,
)
from flask_sqlalchemy import SQLAlchemy
import pyrez
from pyrez.api import *
from pyrez.exceptions import (
  PlayerNotFound,
  MatchException,
)
from pyrez.exceptions.PrivatePlayer import PrivatePlayer
from pyrez.exceptions.ServiceUnavailable import ServiceUnavailable
from pyrez.enumerations import (
  Champions,
  Tier,
)
import requests
from sqlalchemy.exc import (
  IntegrityError,
  InternalError,
  OperationalError,
  ProgrammingError,
)

from langs import *
from app.utils import (
  get_env,
)
from app.lang import (
  get_language,
)
'''
from models.paladins_player import PaladinsPlayer
from models.smite_player import SmitePlayer
from models.session import Session
from models import db
'''

app = Flask(__name__, static_folder='static', template_folder='templates', static_url_path='', instance_relative_config=True) #https://stackoverflow.com/questions/4239825/static-files-in-flask-robot-txt-sitemap-xml-mod-wsgi
with app.app_context() as current_app:
  def get_config(x=None):
    return 'config.' + {
      'development': 'DevelopementConfig',
      'dev': 'DevelopementConfig',
      'testing': 'TestingConfig',
      'default': 'ProductionConfig',
      'production': 'ProductionConfig',
      'prod': 'ProductionConfig'
    }.get(str(x).lower(), 'ProductionConfig')
  #init_db()
  #current_app.push()
  app.config.from_object(get_config(get_env('FLASK_ENV', default='dev' if os.sys.platform == 'win32' else 'prod')))# object-based default configuration
  app.config.from_pyfile('config.cfg', silent=True)#https://flask.palletsprojects.com/en/1.1.x/config/
  print(app.secret_key)
  db = SQLAlchemy(app)

  from app import register
  register(app)
  '''
  from app.overwatch import register as overwatch_register
  from app.twitch import register as twitch_register
  from app.smite import register as smite_register
  from app.youtube import register as youtube_register
  from app.views import blueprint
  for _ in [overwatch_register, smite_register, twitch_register, youtube_register]:
    _(app)
  app.register_blueprint(blueprint, url_prefix='/api')
  '''

class Session(db.Model):
  __tablename__ = 'session'
    
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  sessionId = db.Column(db.String(50), unique=True, nullable=False)
  def __init__(self, sessionId):
    self.sessionId = sessionId
    self.save()
  def __repr__(self):
    return f'<Session {self.sessionId}>'
  def save(self):
    try:
      for sess in Session.query.all():
        sess.delete()
      db.session.add(self)
      db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
      db.session.rollback()
  def update(self, name):
    self.name = name
    db.session.commit()
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def json(self):
    return { 'session_id': self.sessionId }
class Player(db.Model):
  __tablename__ = 'players'
    
  id = db.Column('player_id', db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=False)
  name = db.Column('player_name', db.String(120), nullable=False)
  platform = db.Column('player_platform', db.String(4), nullable=False)

  def __init__(self, id, name, platform):
    self.id = id
    self.name = name
    self.platform = platform
    self.save()
  def __repr__(self):
    return f'<Player {self.name} (Id: {self.id} - Platform: {self.platform})>'
  def save(self):
    try:
      db.session.add(self)
      db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
      db.session.rollback()
      _player = Player.query.filter_by(id=self.id).first()
      _player.delete()
      self.save()
  def update(self, name):
    self.name = name
    db.session.commit()
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def json(self):
    return { 'player_id': self.id, 'player_name': self.name, 'player_platform': self.platform }
class BaseEnumeration(Enum):
  def __str__(self):
    return str(self.value).lower()
  def __hash__(self):
    return hash(str(self.value).lower())
class LanguagesSupported(BaseEnumeration):
  English = 'en'
  Portuguese = 'pt'
  Spanish = 'es'
  Polish = 'pl'
class PlatformsSupported(BaseEnumeration):
  PC = 'pc'
  PTS = 'pts'
  Xbox = '10'
  PS4 = '9'
  Switch = '22'
  Epic = '28'
def sessionCreated(session):
  _session = Session(sessionId=session.sessionId)
try:
  last_session = Session.query.first()
except (OperationalError, ProgrammingError) as e:
  last_session = None
  db.create_all()
  print(e)
finally:
  if hasattr(last_session, 'sessionId'):
    last_session = last_session.sessionId
  print('Paladins Session: ', last_session)
paladinsAPI = PaladinsAPI(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID'), sessionId=last_session or None)

@app.context_processor
def utility_processor():
  return { 'current_time': datetime.now(), 'current_year': datetime.utcnow().year}

@app.errorhandler(404)
def not_found_error(error=None):
  return INTERNAL_ERROR_404_STRINGS[g._language_], 200 #return render_template('404.html'), 404 #return INTERNAL_ERROR_404_STRINGS[g._language_], 404
@app.errorhandler(500)
def internal_error(error=None):
  return INTERNAL_ERROR_500_STRINGS[g._language_], 200 #return render_template('500.html'), 500 #return INTERNAL_ERROR_500_STRINGS[g._language_], 500
@app.before_first_request
def before_first_request_func():
  paladinsAPI.onSessionCreated += sessionCreated

@app.before_request
def before_request_():
  g._language_id_ = get_language(request)
  g._language_ = str(g._language_id_)
'''
@app.after_request
def after_request(response):
  if hasattr(g, '_player_name_'):
    print(g._player_name_)
  return response
'''

@app.route('/api', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['GET'])
def root():
  """Homepage route."""
  return render_template(f'index-{g._language_}.html', lang=g._language_) #redirect(url_for('index'))
def formatDecimal(data, form = ',d'):
  return format(data, form) if data else 0
#def encodeData(data):#https://www.urlencoder.io/python/
#  from urllib.parse import quote as URLEncoder #quote_plus
#  return URLEncoder(data)

def getUrl(endpoint, params=None, _external=True):
  _url = url_for(endpoint, _external=_external)
  for param in params:
    _url = _url.replace(param, '')
  return _url
def getAcceptedLanguages(request_args):
  return str(request_args.accept_languages).split('-')[0] if request_args.accept_languages else LanguagesSupported.English.value
def getLanguage(request_args):
  aux = str(request_args.args.get('language', default=getAcceptedLanguages(request_args))).lower()
  try:
    return LanguagesSupported(aux).value
  except ValueError:
    return LanguagesSupported.English.value
def getChampName(request_args):
  qry = request_args.get('query', default=None)
  champName = request.args.get('champion', None) if not qry else qry[qry.rfind('"')+1:].split(' ') if qry.rfind('"') > 1 else qry.split(' ')
  if isinstance(champName, (type(()), type([]))):
    try:
      champName = champName[1]
    except IndexError:
      champName = None
  #return 'bombking' if 'bk' or 'bomb' in champName else 'maldamba' if 'mal' in champName else champName.lower().replace(' ', '').replace("'", '') if champName else None
  return champName.lower().replace(' ', '').replace("'", "") if champName else None
def printException(exc):
  print('{} : {} : {} : {}'.format(type(exc), exc.args, exc, str(exc)))
def getPlatform(request_args):
  qry = request_args.get('query', default=None)
  if qry:
    aux = qry[qry.rfind('"')+1:].split(' ') if qry.rfind('"') > 1 else qry.split(' ')
    if isinstance(aux, (type(()), type([]))) and len(aux) > 1:
      aux = aux[len(aux) - 1]
    else:
      aux = str(request_args.get('platform', default=None)).lower()
  else:
    aux = str(request_args.get('platform', default=None)).lower()
  if aux.startswith('xb'):
    return PlatformsSupported.Xbox
  if aux.startswith('switch'):
    return PlatformsSupported.Switch
  if aux.startswith('ps'):
    return PlatformsSupported.PS4
  if aux.startswith('pts'):
    return PlatformsSupported.PTS
  if aux.startswith('ep'):
    return PlatformsSupported.Epic
  return PlatformsSupported.PC
def getPlayerName(request_args):
  qry = request_args.get('query', default=None)
  if qry:
    playerName = qry[1:qry.rfind('"')] if qry.rfind('"') > 1 else qry.split(' ')[0]
  else:
    playerName = request_args.get('player', default=None)#str(request_args.get('query', default=str(request_args.get('player', default=None)).lower()).split(' ')[0]).lower()
  if not playerName or len(playerName) < 4 or playerName.lower() in ['$(queryencode%20$(1:)', 'none', '0', 'null', '$(1)', 'query=$(querystring)', '[invalid%20variable]', 'your_ign', '$target']:
    playerName = None
  if playerName:
    playerName = escape(playerName)
  g._player_name_ = playerName or None
  return playerName 
def getPlayerId(playerName, platform = PlatformsSupported.PC):
  if not playerName or playerName in ['$(queryencode%20$(1:)', 'none', '0', 'null', '$(1)', 'query=$(querystring)', '$(querystring)', '[invalid%20variable]', 'your_ign', '$target']:
    return 0
  playerName = playerName.lower()
  if str(playerName).isnumeric():
    return playerName if len(str(playerName)) > 5 or len(str(playerName)) < 12 else 0
  if platform == PlatformsSupported.PC:
    playerName = playerName.strip()#.strip(',.-')
  _player = Player.query.filter_by(name=playerName, platform=str(platform)).first()
  if not _player:
    temp = paladinsAPI.getPlayerId(playerName, platform) if str(platform).isnumeric() else paladinsAPI.getPlayerId(playerName)
    if not temp:
      return -1
    _player = Player(name=playerName, id=temp[0].playerId, platform=str(platform))
  return _player.id if _player else -1
def getInName(player):
  try:
    return (player.hzPlayerName or player.hzGamerTag) or player.playerName
  except Exception:
    pass
  return player.playerName
def getLastSeen(lastSeen, language = LanguagesSupported.English):
  delta = datetime.utcnow() - lastSeen
  hours, remainder = divmod(int(delta.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)
  years, days = divmod(days, 365)
  fmt = '{y}y, {d}d' if years else '{d}d, {h}h' if days else '{h}h, {m}m' if hours else '{m}m, {s}s'
  return fmt.format(y=years, d=days, h=hours, m=minutes, s=seconds)

@app.route('/api/deck', methods=['GET'])
@app.route('/api/decks', methods=['GET'])
def getDecks():
  try:
    championName, playerName, platform = getChampName(request.args), getPlayerName(request.args), getPlatform(request.args)
        
    if not championName:
      return CHAMP_NULL_STRINGS[g._language_]
    playerId = getPlayerId(playerName, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[g._language_] if not playerId else PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
    playerLoadouts = paladinsAPI.getPlayerLoadouts(playerId, int(g._language_id_))
    if len(playerLoadouts) <= 1: #playerLoadouts is None:
      return DONT_HAVE_DECKS_STRINGS[g._language_].format(playerName, championName.capitalize())
    cds = ''
    #lambda n: []
    #nums = [str(n) for n in range(20)]
    #print ''.join(nums)
    loadouts = [playerLoadout for playerLoadout in playerLoadouts if playerLoadout.godName.lower().replace(' ', '').replace("'", "") == championName.lower()]
    for loadout in loadouts:
      cardStr = '{}{}: {}'.format (' ' if len(cds) == 0 else ' · ', loadout.deckName, ['{0} {1}'.format(card.itemName, card.points) for card in loadout.cards]).replace("'", "")
      if len(cds + cardStr) <= 400:
        cds += cardStr
    return cds if cds != '' else DONT_HAVE_DECKS_STRINGS[g._language_].format(playerName, championName)
  #except NoResult as exc:
  #  print('{} : {} : {} : {}'.format(type(exc), exc.args, exc, str(exc)))
  #  return 'Maybe “{}” profile isn't public.'.format(playerName)
  #except requests.exceptions.HTTPError as exc:
  #  printException(exc)
  #  return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[g._language_]
@app.route('/api/version', methods=['GET'])
def getGameVersion():
  try:
    platform = getPlatform(request.args)

    hiRezServerStatus = paladinsAPI.getServerStatus()
    hiRezServerStatus = hiRezServerStatus[1] if platform == PlatformsSupported.Xbox or platform == PlatformsSupported.Switch else hiRezServerStatus[len(hiRezServerStatus) - 2] if platform == PlatformsSupported.PS4 else hiRezServerStatus[len(hiRezServerStatus) - 1] if platform == PlatformsSupported.PTS else hiRezServerStatus[0]
    patchInfo = paladinsAPI.getPatchInfo()
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except Exception as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  return GAME_VERSION_STRINGS[g._language_].format('Paladins', 'Xbox One' if platform == PlatformsSupported.Xbox else 'PS4' if platform == PlatformsSupported.PS4 else 'Nintendo Switch' if platform == PlatformsSupported.Switch else 'PTS' if platform == PlatformsSupported.PTS else 'PC',
    PALADINS_UP_STRINGS[g._language_].format(PALADINS_LIMITED_ACCESS_STRINGS[g._language_] if hiRezServerStatus.limitedAccess else '') if hiRezServerStatus.status else PALADINS_DOWN_STRINGS[g._language_],
    patchInfo.gameVersion, hiRezServerStatus.version)
@app.route('/api/stalk', methods=['GET'])
def getStalk():
  try:
    playerName, platform = getPlayerName(request.args), getPlatform(request.args)

    playerId = getPlayerId(playerName, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[g._language_] if not playerId else PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
    getPlayerRequest = paladinsAPI.getPlayer(playerId)
    playerStalkRequest = paladinsAPI.getPlayerStatus(playerId)
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except PlayerNotFound as exc:
    printException(exc)
    return PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
  except PrivatePlayer as exc:
    printException(exc)
    return PRIVATE_PLAYER_STRINGS[g._language_].format(playerName)
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[g._language_]
  return PLAYER_STALK_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel),
    playerStalkRequest.statusString.replace('God', 'Champion').replace('_', ' ') if playerStalkRequest.status != 3 else CURRENTLY_MATCH_STRINGS[g._language_].format(QUEUE_IDS_STRINGS[g._language_][playerStalkRequest.queueId], playerStalkRequest.matchId),
    getPlayerRequest.createdDatetime.strftime(HOUR_FORMAT_STRINGS[g._language_]), getPlayerRequest.last_login, formatDecimal(getPlayerRequest.hoursPlayed), getPlayerRequest.platform, PLAYER_REGION_STRINGS[g._language_][str(getPlayerRequest.playerRegion).replace(' ', '_').upper()])
@app.route('/api/lastmatch', methods=['GET'])
@app.route('/api/last_match', methods=['GET'])
def getLastMatch():
  try:
    playerName, platform = getPlayerName(request.args), getPlatform(request.args)

    playerId = getPlayerId(playerName, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[g._language_] if not playerId else PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
    lastMatchRequest = paladinsAPI.getMatchHistory(playerId)
    if not lastMatchRequest or not len(lastMatchRequest) > 0:
      raise MatchException
    lastMatchRequest = lastMatchRequest[0]    
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except MatchException as exc:
    printException(exc)
    return PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[g._language_]
  kda = ((lastMatchRequest.assists / 2) + lastMatchRequest.kills) / lastMatchRequest.deaths if lastMatchRequest.deaths > 1 else 1
  kda = int(kda) if kda % 2 == 0 else round(kda, 2)
  return LAST_MATCH_STRINGS[g._language_].format(lastMatchRequest.mapName, lastMatchRequest.matchId, lastMatchRequest.godId.getName() if isinstance(lastMatchRequest.godId, Champions) else lastMatchRequest.godName,
    lastMatchRequest.kills, lastMatchRequest.deaths, lastMatchRequest.assists, kda, lastMatchRequest.killingSpree,
    formatDecimal(lastMatchRequest.damage), formatDecimal(lastMatchRequest.credits), lastMatchRequest.matchMinutes,
    PLAYER_REGION_STRINGS[g._language_][str(lastMatchRequest.matchRegion).replace(' ', '_').upper()], MATCH_STRINGS[g._language_][str(lastMatchRequest.winStatus).upper()], '{0}/{1}'.format(lastMatchRequest.team1Score,
    lastMatchRequest.team2Score) if lastMatchRequest.taskForce == 1 else "{0}/{1}".format(lastMatchRequest.team2Score, lastMatchRequest.team1Score))
@app.route('/api/currentmatch', methods=['GET'])
@app.route('/api/current_match', methods=['GET'])
@app.route('/api/livematch', methods=['GET'])
@app.route('/api/live_match', methods=['GET'])
def getCurrentMatch():
  try:
    playerName, platform, reg = getPlayerName(request.args), getPlatform(request.args), request.args.get('region', None)

    playerId = getPlayerId(playerName, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[g._language_] if not playerId else PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
    playerStatusRequest = paladinsAPI.getPlayerStatus(playerId)
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[g._language_]
  if playerStatusRequest.status != 3:
    return PLAYER_NOT_MATCH_STRINGS[g._language_][playerStatusRequest.status].format(playerName)
  if not playerStatusRequest.queueId.isLiveMatch:#not (playerStatusRequest.queueId.isLiveMatch() or playerStatusRequest.queueId.isPraticeMatch()):
    return QUEUE_ID_NOT_SUPPORTED_STRINGS[g._language_].format(QUEUE_IDS_STRINGS[g._language_][playerStatusRequest.queueId], playerName)
  team1, team2 = [], []
  try:
    players = paladinsAPI.getMatch(playerStatusRequest.matchId, True)
  except LiveMatchException as exc:
    printException(exc)
    return QUEUE_ID_NOT_SUPPORTED_STRINGS[g._language_].format(QUEUE_IDS_STRINGS[g._language_][playerStatusRequest.queueId], playerName)
  if players:
    for player in players:
      if playerStatusRequest.queueId in [ 428, 486 ]:
        rank = PLAYER_RANK_STRINGS[g._language_][player.tier] if player.tier != 0 else PLAYER_RANK_STRINGS[g._language_][0] if player.tierWins + player.tierLosses == 0 else QUALIFYING_STRINGS[g._language_]
      else:
        if player.playerId != '0': #int(player.playerId) != 0:
          if player.accountLevel >= 15:
            getPlayer = paladinsAPI.getPlayer(player.playerId)
            rank = PLAYER_RANK_STRINGS[g._language_][getPlayer.rankedKeyboard.currentRank if getPlayer.rankedKeyboard.hasPlayed else getPlayer.rankedController.currentRank]
          else:
            rank = PLAYER_RANK_STRINGS[g._language_][0]
        else:
          rank = '???'
      if player.taskForce == 1:
        team1.append(CURRENT_MATCH_PLAYER_STRINGS[g._language_].format(player.playerName or '???', player.godName, rank))
      else:
        team2.append(CURRENT_MATCH_PLAYER_STRINGS[g._language_].format(player.playerName or '???', player.godName, rank))
    #try:
    #  __region = PLAYER_REGION_STRINGS[g._language_][str(players[0].playerRegion).replace(' ', '_').upper()]
    #except:
    #  __region = players[0].playerRegion
    __region = players[0].playerRegion
    x_ = '{} - {}'.format(__region, QUEUE_IDS_STRINGS[g._language_][playerStatusRequest.queueId]) if reg else QUEUE_IDS_STRINGS[g._language_][playerStatusRequest.queueId]
    return CURRENT_MATCH_STRINGS[g._language_].format(players[0].getMapName(True), x_, ','.join(team1), ','.join(team2))
  return INTERNAL_ERROR_500_STRINGS[g._language_]
def genRank(rank, lang, rank_only=False):
  if rank_only:
    PLAYER_RANK_STRINGS[lang][rank.currentRank.value] if rank.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[lang][0] if rank.wins + rank.losses == 0 else QUALIFYING_STRINGS[lang]
  return '{}{} {}'.format(PLAYER_RANK_STRINGS[lang][rank.currentRank.value] if rank.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[lang][0] if rank.wins + rank.losses == 0 else QUALIFYING_STRINGS[lang],
    '' if rank.currentRank == Tier.Unranked or rank.currentTrumpPoints <= 0 else ' ({0} TP{1})'.format(formatDecimal(rank.currentTrumpPoints), ON_LEADERBOARD_STRINGS[lang].format(rank.leaderboardIndex) if rank.leaderboardIndex > 0 else ''),
    WINS_LOSSES_STRINGS[lang].format(formatDecimal(rank.wins), formatDecimal(rank.losses)))

@app.route('/api/rank', methods=['GET'])
def getRank():
  try:
    playerName, platform = getPlayerName(request.args), getPlatform(request.args)

    playerId = getPlayerId(playerName, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[g._language_] if not playerId else PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
    getPlayerRequest = paladinsAPI.getPlayer(playerId)
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except PlayerNotFound as exc:
    printException(exc)
    return PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
  except PrivatePlayer as exc:
    printException(exc)
    return PRIVATE_PLAYER_STRINGS[g._language_].format(playerName)
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[g._language_]
  r1, r2 = getPlayerRequest.rankedController, getPlayerRequest.rankedKeyboard
  if r1.hasPlayed and r2.hasPlayed:
    return '{} is {}. | {}. (Win rate Global: {}%, 🖥 Ranked: {}% & 🎮 Ranked: {}%)'.format(PLAYER_LEVEL_STRINGS['en'].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel),
      genRank(r2, 'en'), #genRank(r2, g._language_),
      genRank(r1, 'en'),#genRank(r1, g._language_),
      getPlayerRequest.winratio, r2.winratio, r1.winratio)
  if r2.hasPlayed:
    return PLAYER_GET_RANK_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel),
      PLAYER_RANK_STRINGS[g._language_][r2.currentRank.value] if r2.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[g._language_][0] if r2.wins + r2.losses == 0 else QUALIFYING_STRINGS[g._language_],
      '' if r2.currentRank == Tier.Unranked or r2.currentTrumpPoints <= 0 else ' ({0} TP{1})'.format(formatDecimal(r2.currentTrumpPoints), ON_LEADERBOARD_STRINGS[g._language_].format(r2.leaderboardIndex) if r2.leaderboardIndex > 0 else ''),
      '' if r2.currentRank == Tier.Unranked and r2.wins + r2.losses == 0 else WINS_LOSSES_STRINGS[g._language_].format(formatDecimal(r2.wins), formatDecimal(r2.losses)),
      ' (Win rate Global: {0}%{1})'.format (getPlayerRequest.winratio, '' if r2.wins + r2.losses == 0 else ' & 🖥 Ranked: {0}%'.format(r2.winratio)))
  return PLAYER_GET_RANK_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel),
      PLAYER_RANK_STRINGS[g._language_][r1.currentRank.value] if r1.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[g._language_][0] if r1.wins + r1.losses == 0 else QUALIFYING_STRINGS[g._language_],
      '' if r1.currentRank == Tier.Unranked or r1.currentTrumpPoints <= 0 else ' ({0} TP{1})'.format(formatDecimal(r1.currentTrumpPoints), ON_LEADERBOARD_STRINGS[g._language_].format(r1.leaderboardIndex) if r1.leaderboardIndex > 0 else ''),
      '' if r1.currentRank == Tier.Unranked and r1.wins + r1.losses == 0 else WINS_LOSSES_STRINGS[g._language_].format(formatDecimal(r1.wins), formatDecimal(r1.losses)),
      ' (Win rate Global: {0}%{1})'.format(getPlayerRequest.winratio, '' if r1.wins + r1.losses == 0 else ' & 🎮 Ranked: {0}%'.format(r1.winratio)))
@app.route('/api/winrate', methods=['GET'])
@app.route('/api/kda', methods=['GET'])
def getWinrate():
  try:
    championName, playerName, platform = getChampName(request.args), getPlayerName(request.args), getPlatform(request.args)
        
    playerId = getPlayerId(playerName, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[g._language_] if not playerId else PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
    getPlayerRequest = paladinsAPI.getPlayer(playerId)
    if getPlayerRequest.accountLevel <= 5:
      return PLAYER_LOW_LEVEL_STRINGS[g._language_]
    playerGlobalKDA = paladinsAPI.getChampionRanks(playerId)
  except ServiceUnavailable as exc:
    printException(exc)
    return UNABLE_TO_CONNECT_STRINGS[g._language_]
  except (PlayerNotFound, PrivatePlayer) as exc:
    printException(exc)
    return PLAYER_NOT_FOUND_STRINGS[g._language_].format(playerName)
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[g._language_]
  if not platform == championName and championName:
    for champ in playerGlobalKDA:
      if champ.godName.lower().replace(' ', '').replace("'", "") == championName.lower():
        return CHAMP_WINRATE_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(champ.godName.replace("'", " "), champ.godLevel), champ.wins, champ.losses,
          formatDecimal(champ.kills), formatDecimal(champ.deaths), formatDecimal(champ.assists), champ.kda, champ.winratio)
    return CHAMP_NOT_PLAYED_STRINGS[g._language_].format(playerName, championName)
  deaths, kills, assists = 0, 0, 0
  for champ in playerGlobalKDA:
    kills += champ.kills
    deaths += champ.deaths
    assists += champ.assists
  kda = ((assists / 2) + kills) / deaths if deaths > 1 else 1
  return CHAMP_WINRATE_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel), getPlayerRequest.wins, getPlayerRequest.losses,
    formatDecimal(kills), formatDecimal(deaths), formatDecimal(assists), int(kda) if kda % 2 == 0 else round(kda, 2), getPlayerRequest.winratio)
if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], use_reloader=app.config['DEBUG'])
  #port = int(os.getenv('PORT', 5000))
  #print('Starting app on port %d' % port)
  #app.run(debug=DEBUG, port=port, host='0.0.0.0')
#release: python manage.py db migrate | upgrade
