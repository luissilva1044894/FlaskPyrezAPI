#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

from ..utils import replace

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.route('/rank', methods=['GET'])
def _rank_viewer_route():
	return '!'

#https://github.com/iforvard/SmiteLiveMatchCheck/blob/master/SLMChek.py
#https://cors-anywhere.herokuapp.com/
#https://github.com/enchom/chatbot-smite-api/blob/master/chatbot-smite-api/Smite_Api.py
#https://github.com/enchom/chatbot-smite-api/blob/master/chatbot-smite-api/Smite_StreamlabsSystem.py
#!godrank <player> <god> 'Player {} on {} stats: Worshippers: {} | Win/Loss: {}/{} | Kills/Deaths: {}/{}'.format(player, god, god_rank['Worshippers'], god_rank['Wins'], god_rank['Losses'], god_rank['Kills'], god_rank['Deaths'])
#!duelrank Player {} is in {}'.format(player, Division.get_name(player_data['RankedDuel']['Tier']).replace('_', ' '))
