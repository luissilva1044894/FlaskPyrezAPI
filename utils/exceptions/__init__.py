#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

class CustomException(Exception):
  """
  @app.route('/foo')
  def get_foo():
    raise CustomException('This view is gone', status_code=410)
  """
  status_code = 404

  def __init__(self, message=None, status_code=None, payload=None, *args, **kwargs):
    Exception.__init__(self, *args, **kwargs)
    self.message = message
    if status_code:
      self.status_code = status_code
    self.payload = payload
  def jsonify(self):
    response = jsonify(self.to_dict())
    response.status_code = self.status_code
    return response
  def to_dict(self):
    rv = dict(self.payload or ())
    rv['message'] = self.message
    return rv
