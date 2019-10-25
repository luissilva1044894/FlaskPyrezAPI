#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

blueprint = Blueprint('overwatch', __name__, static_folder='static', template_folder='templates', static_url_path='')

from ..utils import getPlatform, getPlayerName, PlatformsSupported, LanguagesSupported, winratio
#api.add_child(blueprint)

@blueprint.route('/', methods=['GET'])
def index():
	print('??')

	return "Hello World!"

def getRankName(skill_rating):
	if skill_rating <= 1499:
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
	playerName, platform, paladins_like = getPlayerName(request.args), getPlatform(request.args), request.args.get('wr', False)
	import requests
	_json = requests.get('https://ow-api.com/v1/stats/{}/{}/{}/profile'.format(platform, 'us', playerName.replace('#', '-')))
	if _json.ok:

		_json = _json.json()
		_ratings = []
		if _json['private']:
			return "Error: Private account!"
		for x in _json['ratings']:
			_ratings.append('{} {} SR'.format(x['role'].title(), x['level']))
		_rat = ' | '.join(_ratings)
		if paladins_like:
			return "{} is {} ({} SR{}) with {} wins and {} losses. (Win rate: {}%)".format(_json['name'].split('#')[0], getRankName(_json['rating']), _json['rating'], ' - {}'.format(_rat) if _rat else '', _json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played'] - _json['competitiveStats']['games']['won'], winratio(_json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played']))
		return "{} is {} ({} SR){}".format(_json['name'].split('#')[0], getRankName(_json['rating']), _json['rating'], ' - {}'.format(_rat) if _rat else '')
	return "ERROR"
