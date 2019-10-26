#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

blueprint = Blueprint('overwatch', __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.route('/rank', methods=['GET'])
def rank():
	from ..utils import getPlatform, getPlayerName
	from .controllers import rank_function

	return rank_function(getPlayerName(request.args), getPlatform(request.args), request.args.get('wr', False), request.args.get('average_sr', False))
