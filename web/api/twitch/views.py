#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, current_app
from urllib.parse import unquote

from utils.web import create_blueprint, is_async

#blueprint = Blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))
blueprint = create_blueprint(__name__.split('.', 1)[1], __name__, static_url_path='', url_prefix='/{}'.format(__name__.split('.', 1)[1].replace('.views', '').replace('.', '/')))

def get_page():
  return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
  """Homepage route."""
  return jsonify([_ for _ in sorted(unquote('{:50s} {:20s} {}'.format(r.endpoint, ','.join(r.methods), r)) for r in current_app.url_map.iter_rules())])

@blueprint.route('/random_viewer/', methods=['GET'])
def random_viewer_handler():
  return get_page()
