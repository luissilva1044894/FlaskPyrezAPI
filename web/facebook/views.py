#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.web import create_blueprint

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', url_prefix='/{}'.format('/'.join(__blueprint__name[:-1])))

@blueprint.route('/', methods=['GET'])
def health():
	from flask import jsonify
	return jsonify({'status': 'ok', 'msg': "Hello there, I'm a facebook messenger bot."})
