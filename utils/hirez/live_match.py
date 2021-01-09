#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyrez

from . import (
  get_player_id,
  get_player_name,
  PLAYER_RANK_STRINGS,
)
from ..num import format_decimal

def live_match_func(player, platform, lang, api):
  player_id = get_player_id(api, player, platform)
  if not player_id or player_id == -1:
    raise pyrez.exceptions.PrivatePlayer(player)
  player_status_request = api.getPlayerStatus(player_id)
  if player_status_request.status != 3:
    return {
    0: '🚫 ERROR: “{player}” is Offline.',
    1: '🚫 ERROR: “{player}” is still in Lobby.',
    2: '🚫 ERROR: “{player}” is still selecting a champion. You need to wait until the match has started.',
    4: '🚫 ERROR: “{player}” is Online, but not in a match.',
    5: "🚫 ERROR: “{player}” doesn't exist or it's hidden.",
  }[player_status_request.status].format(player=player)
  team1, team2, players = [], [], api.getMatch(player_status_request.matchId, True)
  if players:
    for player in (players or []):
      if player_status_request.queueId in [ 448, 451, 450, 502, 440, 428, 486 ]:
        rank = PLAYER_RANK_STRINGS[lang][player.tier] if player.tier != 0 else PLAYER_RANK_STRINGS[lang][0]
      else:
        if hasattr(player, 'playerId') and player.playerId not in ['0', 0]:
          if player.accountLevel >= 15:
            getPlayer = api.getPlayer(player.playerId)
            if hasattr(getPlayer, 'rankedConquestController'):
              rank = PLAYER_RANK_STRINGS[lang][getPlayer.rankedConquestController.currentRank if getPlayer.rankedConquestController.hasPlayed else getPlayer.rankedConquest.currentRank]
            else:
              rank = PLAYER_RANK_STRINGS[lang][getPlayer.rankedController.currentRank if getPlayer.rankedController.hasPlayed else getPlayer.rankedKeyboard.currentRank]
          else:
            rank = PLAYER_RANK_STRINGS[lang][0]
        else:
          rank = '???'
      if player.taskForce == 1:
        team1.append(f'{get_player_name(player) or "???"}: {player.godName} ({rank})')
      else:
        team2.append(f'{get_player_name(player) or "???"}: {player.godName} ({rank})')
    return f'{players[0]["mapGame"] or players[0].getMapName(True)}: {", ".join(team1)} · VS · {", ".join(team2)}'.replace('()', '').replace(' : ', ': ')
  return ''
