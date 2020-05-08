#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  Blueprint,
  g,
  render_template,
  request,
)

from .controllers.rank import rank_func
from .controllers.patch_notes import patch_notes_func
from ..utils import (
  fix_url_for,
  get_json,
  getPlatform,
  getPlayerName,
  get_query,
  replace,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.errorhandler(404)
@blueprint.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(g._language_), blueprint.name), lang=g._language_, my_name=blueprint.name.upper())

@blueprint.route('/patch_notes', methods=['GET'])
def patch_notes_handler():
  return patch_notes_func()

@blueprint.route('/rank', methods=['GET'])
def rank_handler():
  print(get_query(request.args, 'wr', False))
  print(get_query(request.args, 'average_sr', False))

  return rank_func(getPlayerName(request.args), getPlatform(request.args), get_query(request.args, 'wr', False), get_query(request.args, 'average_sr', False))
