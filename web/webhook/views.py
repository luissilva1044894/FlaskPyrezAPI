#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from utils import replace

blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='')#'/'

@blueprint.route('/webhook/', methods=['GET', 'POST'])
def webhook_handler():
	from flask import jsonify, request
	if request.method == 'GET':
		if request.args.get('hub.verify_token', None):
			return request.args.get('hub.challenge')
	return jsonify(status='ok', name=blueprint.name)#{'status': 'ok'}

