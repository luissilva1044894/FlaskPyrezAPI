#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  Blueprint,
  render_template,
  request,
)

from .controllers import rank_func
from ..utils import (
  fix_url_for,
  get_json,
  get_language,
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
  print(blueprint.root_path)
  lang = get_language(request)
  return render_template('new_index.html'.format(blueprint.name.lower()), _json=fix_url_for(get_json(lang), blueprint.name), lang=lang, my_name=blueprint.name.upper())

@blueprint.route('/rank', methods=['GET'])
def rank_handler():
  print(get_query(request.args, 'wr', False))
  print(get_query(request.args, 'average_sr', False))

  return rank_func(getPlayerName(request.args), getPlatform(request.args), get_query(request.args, 'wr', False), get_query(request.args, 'average_sr', False))
