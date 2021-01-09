#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyrez

from . import (
  get_player_id,
  get_player_name,
  PLAYER_RANK_STRINGS,
)
from ..num import format_decimal

def gen_rank(rank, lang, rank_only=False):
  if rank_only:
    PLAYER_RANK_STRINGS[lang][rank.currentRank.value] if rank.currentRank != pyrez.enumerations.Tier.Unranked else PLAYER_RANK_STRINGS[lang][0] if rank.wins + rank.losses == 0 else QUALIFYING_STRINGS[lang]
  return '{}{} {}'.format(PLAYER_RANK_STRINGS[lang][rank.currentRank.value] if rank.currentRank != pyrez.enumerations.Tier.Unranked else PLAYER_RANK_STRINGS[lang][0] if rank.wins + rank.losses == 0 else QUALIFYING_STRINGS[lang],
    '' if rank.currentRank == pyrez.enumerations.Tier.Unranked or rank.currentTrumpPoints <= 0 else ' ({0} TP{1})'.format(formatDecimal(rank.currentTrumpPoints), ON_LEADERBOARD_STRINGS[lang].format(rank.leaderboardIndex) if rank.leaderboardIndex > 0 else ''),
    WINS_LOSSES_STRINGS[lang].format(formatDecimal(rank.wins), formatDecimal(rank.losses)))

def rank_func(player, platform, lang, api):
  player_id = get_player_id(api, player, platform)
  if not player_id or player_id == -1:
    raise pyrez.exceptions.PrivatePlayer(player)
  get_player_request = api.getPlayer(player_id)
  #if get_player_request.rankedController.hasPlayed and get_player_request.rankedKeyboard.hasPlayed:
  #  return f'{get_player_name(get_player_request)} (Level {get_player_request.accountLevel}) is {gen_rank(get_player_request.rankedController, 'en')}. | {gen_rank(get_player_request.rankedKeyboard, 'en')}. (Win rate Global: {get_player_request.winratio}%, 🖥 Ranked: {get_player_request.rankedController.winratio}% & 🎮 Ranked: {get_player_request.rankedKeyboard.winratio}%)'

  if hasattr(get_player_request, 'rankedConquestController'):
    rank_ = get_player_request.rankedConquestController if get_player_request.rankedConquestController.hasPlayed else get_player_request.rankedConquest
  else:
    rank_ = get_player_request.rankedController if get_player_request.rankedController.hasPlayed else get_player_request.rankedKeyboard
  if hasattr(get_player_request, 'rankedConquestController'):
    plat_ = '🎮' if get_player_request.rankedConquestController.hasPlayed else '🖥'
  else:
    plat_ = '🎮' if get_player_request.rankedController.hasPlayed else '🖥'
  mmr = f'{round(rank_.rankStat)} MMR, ' if rank_.rankStat else ''
  return f"""{get_player_name(get_player_request)} (Level {get_player_request.accountLevel}) is
  {PLAYER_RANK_STRINGS[lang][rank_.currentRank] if rank_.currentRank != pyrez.enumerations.Tier.Unranked else PLAYER_RANK_STRINGS[lang][0]}
  {'' if rank_.currentRank == pyrez.enumerations.Tier.Unranked or rank_.currentTrumpPoints <= 0 else f'({mmr}{format_decimal(rank_.currentTrumpPoints)} TP, {rank_.leaderboardIndex} on the leaderboard)'}
   with {format_decimal(rank_.wins)} wins and {format_decimal(rank_.losses)} losses.
   (Win rate Global: {get_player_request.winratio}%{'' if rank_.wins + rank_.losses == 0 else f' & {plat_} Ranked: {rank_.winratio}%'})"""
