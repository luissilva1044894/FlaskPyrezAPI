#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .exceptions import PlayerNotFound
from . import (
  get_player_id,
  get_player_name,
)

def kda_func(player, champ, platform, lang, api):
  player_id = get_player_id(api, player, platform)
  if not player_id or player_id == -1:
    raise PlayerNotFound(player)
  get_player_request = api.getPlayer(player_id)
'''
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
  if championName and not championName == getPlatform(championName):
    for champ in playerGlobalKDA:
      if champ.godName.lower().replace(' ', '').replace("'", "") == championName.lower():
        return CHAMP_WINRATE_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(champ.godName.replace("'", " "), champ.godLevel), champ.wins, champ.losses,
          formatDecimal(champ.kills), formatDecimal(champ.deaths), formatDecimal(champ.assists), champ.kda, champ.winratio)
    #return CHAMP_NOT_PLAYED_STRINGS[g._language_].format(playerName, championName) # Maybe uncomment this?
  deaths, kills, assists = 0, 0, 0
  for champ in playerGlobalKDA:
    kills += champ.kills
    deaths += champ.deaths
    assists += champ.assists
  kda = ((assists / 2) + kills) / deaths if deaths > 1 else 1
  return CHAMP_WINRATE_STRINGS[g._language_].format(PLAYER_LEVEL_STRINGS[g._language_].format(getInName(getPlayerRequest), getPlayerRequest.accountLevel), getPlayerRequest.wins, getPlayerRequest.losses,
    formatDecimal(kills), formatDecimal(deaths), formatDecimal(assists), int(kda) if kda % 2 == 0 else round(kda, 2), getPlayerRequest.winratio)
'''