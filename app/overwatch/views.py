#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

blueprint = Blueprint('overwatch', __name__, static_folder='static', template_folder='templates', static_url_path='')

from ..utils import getPlatform, getPlayerName, PlatformsSupported, LanguagesSupported, winratio

def getBattleNet(battle_net):
	return battle_net.replace('#', '-', 1)

def getRankName(skill_rating):
	if skill_rating >= 1 and skill_rating <= 1499:
		return 'Bronze'
	elif skill_rating >= 1500 and skill_rating <= 1999:
		return 'Silver'
	elif skill_rating >= 2000 and skill_rating <= 2499:
		return 'Gold'
	elif skill_rating >= 2500 and skill_rating <= 2999:
		return 'Platinum'
	elif skill_rating >= 3000 and skill_rating <= 3499:
		return 'Diamond'
	elif skill_rating >= 3500 and skill_rating <= 3999:
		return 'Master'
	elif skill_rating >= 4000:
		'Grandmaster'
	return '???'
@blueprint.route('/rank', methods=['GET'])
def rank():
	playerName, platform, paladins_like, format_average_sr = getPlayerName(request.args), getPlatform(request.args), request.args.get('wr', False), request.args.get('average_sr', False)
	import requests
	_json = requests.get('https://ow-api.com/v1/stats/{}/{}/{}/profile'.format(platform, 'us', getBattleNet(playerName)))
	if _json.ok:

		_json = _json.json()
		_ratings = []
		if _json['private']:
			return "Error: Private account!"
		high_sr = -1
		for x in _json['ratings']:
			if x['level'] > high_sr:
				high_sr = x['level']
			_ratings.append('{} {} SR'.format(x['role'].title(), x['level']))
		_rat = ' | '.join(_ratings)
		_rank = _json['rating'] if format_average_sr else high_sr
		if paladins_like:
			return "{} is {} ({} SR{}) with {} wins and {} losses. (Win rate: {}%)".format(_json['name'].split('#')[0], getRankName(_rank), _rank, ' - {}'.format(_rat) if _rat else '', _json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played'] - _json['competitiveStats']['games']['won'], winratio(_json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played']))
		return "{} is {} ({} SR){}".format(_json['name'].split('#')[0], getRankName(_rank), _rank, ' - {}'.format(_rat) if _rat else '')
	return "ERROR"
#valid_regions = ['en-us', 'en-gb', 'es-es', 'es-mx', 'pt-br', 'pl-pl']
#valid_platforms = ['pc', 'psn', 'xbl']

"""
for letter in name:
	if letter == '#':
		name = name.replace(letter, '-')
	elif letter in ('[', ']', '{', '}', '<', '>', '(', ')', '"', '%', '+', '£', '$', '€'):
		name = name.replace(letter, '')
		if platform == 'pc':
			address = f"https://ow-api.com/v1/stats/{platform}/global/{name}/complete"
		else:
			address = f"https://ow-api.com/v1/stats/{platform}/{name}/complete"
"""
