
def random_viewer_function(_channel, _exclude, _ignore):
	from ..utils import get_url
	_json = get_url('http://tmi.twitch.tv/group/user/{}/chatters'.format(_channel))
	for x in str(_ignore).split(','):
		if x.lower() == 'bots':
			_exclude += 'nightbot,priestbot,streamelements,streamlabs,botisimo,moobot'.split(',')
			_exclude += 'twitchprimereminder,commanderroot,anotherttvviewer,electricallongboard'.split(',')
		try:
			_json['chatters'].pop(x)
		except KeyError: #ValueError = _json['bots']
			pass
	_final_list = []
	for x in _json['chatters']:
		for y in _json['chatters'][x]:
			for z in _exclude:
				if str(y).lower() == z.lower():
					try:
						_json['chatters'][x].remove(y)
					except ValueError:
						pass
		if len(_json['chatters'][x]) != 0:
			_final_list += _json['chatters'][x]
	if _final_list:
		from ..utils import random
		return _final_list[random(0, len(_final_list) - 1)]
	return "Error: No viewers"
