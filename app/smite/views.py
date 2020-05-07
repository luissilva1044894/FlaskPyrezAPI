#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
  render_template,
  request,
)

from .controllers import (
  rank_func,
  live_match_func,
)
from ..utils import (
  fix_url_for,
  get_json,
  get_language,
  getPlatform,
  getPlayerName,
  replace,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.errorhandler(404)
@blueprint.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  print(blueprint.root_path)
  lang = get_language(request)
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(lang), blueprint.name), lang=lang, my_name=blueprint.name.upper())

@blueprint.route('/rank', methods=['GET'])
def _rank_viewer_route():
  return rank_func(getPlayerName(request.args), getPlatform(request.args), get_language(request))

@blueprint.route('/currentmatch', methods=['GET'])
@blueprint.route('/current_match', methods=['GET'])
@blueprint.route('/livematch', methods=['GET'])
@blueprint.route('/live_match', methods=['GET'])
def _live_match_route():
  return live_match_func(getPlayerName(request.args), getPlatform(request.args), get_language(request))
#https://github.com/iforvard/SmiteLiveMatchCheck/blob/master/SLMChek.py
#https://cors-anywhere.herokuapp.com/
#https://github.com/enchom/chatbot-smite-api/blob/master/chatbot-smite-api/Smite_Api.py
#https://github.com/enchom/chatbot-smite-api/blob/master/chatbot-smite-api/Smite_StreamlabsSystem.py
#!godrank <player> <god> 'Player {} on {} stats: Worshippers: {} | Win/Loss: {}/{} | Kills/Deaths: {}/{}'.format(player, god, god_rank['Worshippers'], god_rank['Wins'], god_rank['Losses'], god_rank['Kills'], god_rank['Deaths'])
#!duelrank Player {} is in {}'.format(player, Division.get_name(player_data['RankedDuel']['Tier']).replace('_', ' '))
