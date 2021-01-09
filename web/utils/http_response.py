#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Response

def http_response(resp, status, mimetype='application/json', **kw):
  return Response(json.dumps(resp), status=status, mimetype=mimetype, **kw)

def ok_response(resp):
  resp.update({'success': True})
  return HttpResponse(resp, 200)

def not_ok_response(resp):
  resp.update({'success': False})
  return HttpResponse(resp, 400)

DEFAULT_MESSAGES = {
  403: 'Forbidden: You are not authorized to access this resource.',
  500: 'Unknown server error occured.'
}
def error_response(error_code, message=None):
  return jsonify({
    'status': error_code,
    'message': message or DEFAULT_MESSAGES.get(error_code)
  }, status=error_code)

def create_response(data:dict, status:int=200, msg:str=''):
  if not data or not isinstance(data, dict):
    raise TypeError(f'Data should be a dictionary, not {type(data)}')
  response = {
    'code': status,
    'success': 200 <= status < 300,
    'message': msg,
    'result': data,
  }
  return jsonify(response), status
