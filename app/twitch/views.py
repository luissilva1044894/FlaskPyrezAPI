#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

blueprint = Blueprint(__name__.split('.')[1] or __name__.replace('app.', ''), __name__, static_folder='static', template_folder='templates', static_url_path='')


from ..utils import get_query, get_url

@blueprint.route('/random_viewer', methods=['GET'])
@blueprint.route('/random_user', methods=['GET'])
def _randon_viewer_route():
	_channel, _exclude, _ignore = get_query(request.args, 'channel'), str(get_query(request.args, 'exclude')).split(','), get_query(request.args, 'ignore')
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
		import random
		return _final_list[random.randint(0, len(_final_list) - 1)]
	return "Error: No viewers"
