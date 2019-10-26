
def random_viewer_function(_channel, _exclude, _ignore):
	from ..utils import get_url
	_json = get_url('http://tmi.twitch.tv/group/user/{}/chatters'.format(str(_channel).lower()))
	for x in str(_ignore).split(','):
		if x.lower() == 'bots':
			_exclude += 'nightbot,priestbot,streamelements,streamlabs,botisimo,moobot'.split(',')
			_exclude += 'twitchprimereminder,commanderroot,anotherttvviewer,electricallongboard'.split(',')
		elif x.lower() == 'mods':
			x = 'moderators'
		try:
			_json['chatters'].pop(x)
		except (KeyError, TypeError): #ValueError = _json['bots']
			pass
	_final_list = []
	if len(_json) < 1:
		return "The list of users is empty"
	for x in _json['chatters']:
		for y in _json['chatters'][x]:
			for z in _exclude:
				if str(y).lower() == z.lower():
					try:
						_json['chatters'][x].remove(y)
					except (KeyError, TypeError):
						pass
		if len(_json['chatters'][x]) != 0:
			_final_list += _json['chatters'][x]
	if _final_list:
		from ..utils import random
		return _final_list[random(0, len(_final_list) - 1)]
	return "Error: No chatters"#https://community.nightdev.com/t/custom-api-random-viewer/17450/3
