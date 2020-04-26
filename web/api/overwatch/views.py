#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request

from utils.web import create_blueprint, decorators, get
from utils.web.exceptions import PlayerRequired

__blueprint__name = __name__.split('.')[1:]
blueprint = create_blueprint('.'.join(__blueprint__name), __name__, static_url_path='', url_prefix='/{}'.format('/'.join(__blueprint__name[:-1])))

def get_page():
  return ' '.join([blueprint.name, request.url_rule.rule])

@blueprint.route('/', methods=['GET'])
def root_handler(error=None):
  """Homepage route."""
  return get_page()

@blueprint.route('/rank', methods=['GET'], strict_slashes=False)
@decorators.player_required
def rank_handler():
  return get_page()
