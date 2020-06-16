#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  Blueprint,
  g,
  request,
)

from ..utils import replace
from . import get_language

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__)

'''
@blueprint.before_app_first_request
def before_app_first_request_():
  print('before_app_first_request')
'''
@blueprint.before_app_request
def before_app_request_():
  g._language_id_ = get_language(request)
  g._language_ = str(g._language_id_)
