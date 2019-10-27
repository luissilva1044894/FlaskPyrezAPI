#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

from ..utils import replace

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.route('/rank', methods=['GET'])
def rank():
	from ..utils import getPlatform, getPlayerName, get_query
	from .controllers import rank_func

	return rank_func(getPlayerName(request.args), getPlatform(request.args), get_query(request.args, 'wr', False), get_query(request.args, 'average_sr', False))
