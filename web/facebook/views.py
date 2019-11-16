#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from utils import replace

#blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='')#'/'
blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

@blueprint.route('/', methods=['GET'])
def health():
	from flask import jsonify
	return jsonify({'status': 'ok', 'msg': "Hello there, I'm a facebook messenger bot."})
