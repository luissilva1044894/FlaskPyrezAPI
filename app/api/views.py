#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arrow import (
  now,
  utcnow,
)
from flask import request

from utils.web import (
  create_blueprint,
  get_page,
)

api = create_blueprint(__name__)

@api.errorhandler(404)
@api.route('/', methods=['GET'])
def root_handler(error=None):
  #https://gist.github.com/cybertoast/6499708
  '''Self-documenting: Get a list of all routes, and their endpoint's docstrings as a helper resource for API documentation. '''
  return get_page(api)

@api.route('/random/')
def random_handler():
  return 'random'
  _max, _min = try_int(get('max'), 100), try_int('min')
  return str(random(_min, _max, args=[_ for _ in get('query', '').split(',') if _]))

@api.route('/timestamp/')
def server_timestamp_handler():
  """This endpoint returns the current server and UTC time."""
  return { 'local': now().format('DD-MMM-YYYY HH:mm:SS ZZ'), 'unix': now().timestamp, 'utc': utcnow().format('DD-MMM-YYYY HH:mm:SS ZZ') }
