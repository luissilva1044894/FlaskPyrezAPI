#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

from ..utils import replace

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.errorhandler(404)
@blueprint.route('/', methods=['GET'])
def root(error=None):
	"""Homepage route."""
	from ..utils import fix_url_for, get_json
	return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json('pt'), blueprint.name), lang='pt', my_name=blueprint.name.upper())

@blueprint.route('/rank', methods=['GET'])
def rank():
	from ..utils import getPlatform, getPlayerName, get_query
	from .controllers import rank_func

	return rank_func(getPlayerName(request.args), getPlatform(request.args), get_query(request.args, 'wr', False), get_query(request.args, 'average_sr', False))
