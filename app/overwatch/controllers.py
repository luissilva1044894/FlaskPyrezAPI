def get_battle_net(battle_net):
	return battle_net.replace('#', '-', 1)

def get_rank_name(skill_rating):
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

def rank_func(battle_net, platform, paladins_like=False, format_average_sr=False):
	from ..utils import winratio, get_url
	if not battle_net:
		return '🚫 ERROR: Player not specified!'
	
	try:
		#https://github.com/Addonexus/OverwatchWebscraper/blob/master/scraper.py
		from bs4 import BeautifulSoup
		import requests
		import time
		rank = {}
		last_time = time.time()
		for item in BeautifulSoup(requests.get('https://playoverwatch.com/{}/career/{}/{}'.format('en-us', platform, get_battle_net(battle_net))).text, 'html.parser').findAll('div', {'class': 'competitive-rank-role'}):
			rank[str(item.findAll('div', {'class': 'competitive-rank-tier-tooltip'})[0]['data-ow-tooltip-text'].split()[0]).lower()] = int(item.findAll('div', {'class': 'competitive-rank-level'})[0].text)
		curr_time = time.time() - last_time
		print(f'That took {curr_time} seconds')
		print(rank)
	except:
		pass
	else:
		try:
			_ratings, high_sr, __x__, __y__ = [], -1, 0, 0
			for x in rank:
				if format_average_sr:
					__x__ += 1
					__y__ += rank[x]
				if rank[x] > high_sr:
					high_sr = rank[x]
				_ratings.append('{} {} SR'.format(x.title(), rank[x]))
			_rat = ' | '.join(_ratings)
			_rank = __x__ / __y__ if format_average_sr else high_sr
		except:
			pass
		else:
			if rank:
				return '{} is {} ({} SR){}'.format(battle_net.split('-')[0], get_rank_name(_rank), _rank, ' - {}'.format(_rat) if _rat else '')

	_json = get_url('https://ow-api.com/v1/stats/{}/{}/{}/profile'.format(platform, 'us', get_battle_net(battle_net)))
	if isinstance(_json, dict):
		if _json['error']:
			return "🚫 ERROR: " + _json['error']
		if _json['private']:
			return "🚫 ERROR: Private account!"
		_ratings = []
		high_sr = -1
		for x in _json['ratings']:
			if x['level'] > high_sr:
				high_sr = x['level']
			_ratings.append('{} {} SR'.format(x['role'].title(), x['level']))
		_rat = ' | '.join(_ratings)
		_rank = _json['rating'] if format_average_sr else high_sr
		if paladins_like:
			return "{} is {} ({} SR{}) with {} wins and {} losses. (Win rate: {}%)".format(_json['name'].split('#')[0], get_rank_name(_rank), _rank, ' - {}'.format(_rat) if _rat else '', _json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played'] - _json['competitiveStats']['games']['won'], winratio(_json['competitiveStats']['games']['won'], _json['competitiveStats']['games']['played']))
		return "{} is {} ({} SR){}".format(_json['name'].split('#')[0], get_rank_name(_rank), _rank, ' - {}'.format(_rat) if _rat else '')
	return "🚫 ERROR"
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
