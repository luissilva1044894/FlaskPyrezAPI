#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
  render_template,
  request,
)

from .controllers import random_viewer_function
from ..utils import (
  get_query,
  replace,
)

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__, static_folder='static', template_folder='templates', static_url_path='')

@blueprint.route('/random_viewer', methods=['GET'])
@blueprint.route('/random_user', methods=['GET'])
def _random_viewer_route():
  return random_viewer_function(get_query(request.args, 'channel'), str(get_query(request.args, 'exclude')).split(','), get_query(request.args, 'ignore'))
