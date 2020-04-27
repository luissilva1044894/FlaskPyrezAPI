import pyrez
from pyrez.api import *
from pyrez.exceptions import PlayerNotFound, MatchException
from pyrez.exceptions.PrivatePlayer import PrivatePlayer
from pyrez.enumerations import Tier
from pyrez import SmiteAPI
from pyrez.enumerations.QueueSmite import QueueSmite

from ..utils import get_env
from ..utils.num import formatDecimal
from langs import *

from sqlalchemy.exc import OperationalError, ProgrammingError

from models import Session
def sessionCreated(session):
  _session = Session(session_id=session.sessionId)
print('Smite Session: ', last_session.get_session_id())

smiteAPI = SmiteAPI(devId=get_env('PYREZ_DEV_ID'), authKey=get_env('PYREZ_AUTH_ID'), sessionId=last_session.get_session_id())
smiteAPI.onSessionCreated += sessionCreated

S_PLAYER_NOT_FOUND_STRINGS = {
  'en' : "🚫 ERROR: “{0}” doesn't exist or it's hidden! Make sure that your account is marked as “Public Profile”'",
  'es' : '🚫 ERROR: ¡“{0}” no existe o tienes perfil oculto! Make sure that your account is marked as “Public Profile”',
  'pl' : '🚫 BŁĄD: Nie znaleziono gracza “{0}”! Make sure that your account is marked as “Public Profile”',
  'pt' : '🚫 ERRO: “{0}” não existe ou tem perfil privado!',
}

#https://www.twitch.tv/benai
def getPlayerId(playerName, platform=None):
  if not playerName or (playerName in ['none', '0', 'null', '$(1)', 'query=$(querystring)', '[invalid%20variable]', 'your_ign', '$target']):
    return 0
  playerName = playerName.strip().lower()
  if str(playerName).isnumeric():
    return playerName if len(str(playerName)) > 5 or len(str(playerName)) < 12 else 0
  temp = smiteAPI.getPlayerId(playerName, platform) if platform and str(platform).isnumeric() else smiteAPI.getPlayerId(playerName)
  if not temp:
    return -1
  return temp[0].playerId
def getInName(player):
  try:
    return (player.hzPlayerName or player.hzGamerTag) or player.playerName
  except Exception:
    pass
  return player.playerName

def get_rank_name(tier):
  if tier >= 1 and tier <= 5:
    return 'Bronze'
  if tier >= 6 and tier <= 10:
    return 'Silver'
  if tier >= 11 and tier <= 15:
    return 'Gold'
  if tier >= 16 and tier <= 20:
    return 'Platinum'
  if tier >= 21 and tier <= 25:
    return 'Diamond'
  if tier == 26:
    return 'Master'
  if tier == 27:
    return 'Grandmaster'
  if tier == 0:
    return 'Unranked'
  return '???'

def printException(exc):
  print(f'{type(exc)} : {exc.args} : {exc} : {str(exc)}')

#language = 'pt'

def rank_func(player, platform, language='en'):
  try:
    playerId = getPlayerId(player, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[language] if not playerId else S_PLAYER_NOT_FOUND_STRINGS[language].format(player)
    getPlayerRequest = smiteAPI.getPlayer(playerId)
  except PlayerNotFound as exc:
    printException(exc)
    return S_PLAYER_NOT_FOUND_STRINGS[language].format(player)
  except PrivatePlayer as exc:
    printException(exc)
    return S_PLAYER_NOT_FOUND_STRINGS[language].format(player)
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[language]
  r1 = getPlayerRequest.rankedConquest
  return PLAYER_GET_RANK_STRINGS[language].format(PLAYER_LEVEL_STRINGS[language].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel),
      PLAYER_RANK_STRINGS[language][r1.currentRank.value] if r1.currentRank != Tier.Unranked else PLAYER_RANK_STRINGS[language][0] if r1.wins + r1.losses == 0 else QUALIFYING_STRINGS[language],
      '' if r1.currentRank == Tier.Unranked or r1.currentTrumpPoints <= 0 else ' ({2} MMR, {0} TP{1})'.format(formatDecimal(r1.currentTrumpPoints), ON_LEADERBOARD_STRINGS[language].format(r1.leaderboardIndex) if r1.leaderboardIndex > 0 else '', round(r1.rankStat)),
      '' if r1.currentRank == Tier.Unranked and r1.wins + r1.losses == 0 else WINS_LOSSES_STRINGS[language].format(formatDecimal(r1.wins), formatDecimal(r1.losses)),
      ' (Win rate Global: {0}%{1})'.format(getPlayerRequest.winratio, '' if r1.wins + r1.losses == 0 else ' & Ranked: {0}%'.format(r1.winratio)))
  #As informações importantes são essas. Level, Win/Losses, Ranks e RankStats. Para ser sincero, Rank_Stat é mais importante no dia de hoje quando perguntam do elo que ranks

def live_match_func(player, platform, language='en'):
  try:
    playerId = getPlayerId(player, platform)
    if not playerId or playerId == -1:
      return PLAYER_NULL_STRINGS[language] if not playerId else S_PLAYER_NOT_FOUND_STRINGS[language].format(player)
    playerStatusRequest = smiteAPI.getPlayerStatus(playerId)
  except Exception as exc:
    printException(exc)
    return INTERNAL_ERROR_500_STRINGS[language]
  print(playerStatusRequest.status)
  if playerStatusRequest.status != 3:
    return PLAYER_NOT_MATCH_STRINGS[language][playerStatusRequest.status].format(player)
  """
  if not playerStatusRequest.queueId in [ 448, 451, 450, 502, 440, 435, 445 ]:
    print(dir(playerStatusRequest))
    try:
      print(playerStatusRequest.queueId)
      return QUEUE_ID_NOT_SUPPORTED_STRINGS[language].format(QUEUE_IDS_STRINGS[language][playerStatusRequest.queueId], player)
    except KeyError as ex:
      print(ex)
      return QUEUE_ID_NOT_SUPPORTED_STRINGS[language].format('', player)
  """
  team1, team2 = [], []
  try:
    players = smiteAPI.getMatch(playerStatusRequest.matchId, True)
  except LiveMatchException as exc:
    printException(exc)
    return QUEUE_ID_NOT_SUPPORTED_STRINGS[language].format(QUEUE_IDS_STRINGS[language][playerStatusRequest.queueId], player)
  if players:
    for player in players:
      if playerStatusRequest.queueId in [ 448, 451, 450, 502, 440 ]:
        rank = PLAYER_RANK_STRINGS[language][player.tier] if player.tier != 0 else PLAYER_RANK_STRINGS[language][0] if player.tierWins + player.tierLosses == 0 else QUALIFYING_STRINGS[language]
      else:
        if player.playerId != '0': #int(player.playerId) != 0:
          if player.accountLevel >= 15:
            getPlayer = smiteAPI.getPlayer(player.playerId)
            rank = PLAYER_RANK_STRINGS[language][getPlayer.rankedConquest.currentRank]
          else:
            rank = PLAYER_RANK_STRINGS[language][0]
        else:
          rank = '???'
      if player.taskForce == 1:
        team1.append(CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName or '???', player.godName, rank))
      else:
        team2.append(CURRENT_MATCH_PLAYER_STRINGS[language].format(player.playerName or '???', player.godName, rank))
      #x_ = '{} - {}'.format('', QUEUE_IDS_STRINGS[language][playerStatusRequest.queueId]) if reg else QUEUE_IDS_STRINGS[language][playerStatusRequest.queueId]
      x_ = ''#str(QueueSmite(playerStatusRequest.queueId)).replace('_', ' ')
    return CURRENT_MATCH_STRINGS[language].format(players[0].getMapName(True), x_, ','.join(team1), ','.join(team2)).replace('()', '').replace(' : ', ': ')
  return INTERNAL_ERROR_500_STRINGS[language]
