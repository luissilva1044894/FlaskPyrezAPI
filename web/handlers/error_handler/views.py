#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
import requests

from ...utils import (
  create_blueprint,
  exceptions,
)

error_handler = create_blueprint(__name__, template_folder='templates')

@error_handler.app_errorhandler(exceptions.FieldRequired)
def field_required_error_handler(error=None):
  if hasattr(error, 'message') and error.message:
    return f'🚫 ERROR: {error.message}'  
  return f'🚫 ERROR: {error}'

@error_handler.app_errorhandler(404)
def error_404_handler(error):
  return render_template('error_handler/404.html')#str(error), 404

@error_handler.app_errorhandler(403)
def error_403_handler(error):
  return str(error), 403

@error_handler.app_errorhandler(500)
def error_500_handler(error):
  return str(error), 500

@error_handler.app_errorhandler(requests.exceptions.ConnectionError)
def connection_error_handler(error=None):
  return f'ConnectionError: {error}'

@error_handler.app_errorhandler(requests.exceptions.HTTPError)
def http_error_handler(error=None):
  return f'Error: {error}'

'''
@app.errorhandler(Exception)
def handle_error(e):
  code = 500
  if isinstance(e, HTTPException):
    code = e.code
  return jsonify(error=str(e)), code

for ex in default_exceptions:
  app.register_error_handler(ex, handle_error)
'''
