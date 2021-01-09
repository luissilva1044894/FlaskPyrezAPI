#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5

class BaseAPI(object):
  __slots__ = (
    'auth_key',
    'dev_id',
    'endpoint',
    'session',
  )

  def __init__(self, dev_id, auth_key, endpoint, session=None):
    self.auth_key = auth_key
    self.dev_id = dev_id
    self.endpoint = endpoint
    self.session = session

  @property
  def session_id(self):
    if self.session and hasattr(self.session, 'get'):
      return self.session.get('session_id')
    return self.session

  def build_request_url(self, method_name, params=None):
    def fix_param(param):
      if isinstance(param, (list, tuple)):
        return [fix_param(p) for p in param if p]
      if hasattr(param, 'strftime'):
        return param.strftime('%Y%M%d')
      if hasattr(param, 'value'):
        return str(param.value)
      return str(param)
    url = f'{self.endpoint}/{method_name}json'
    if method_name != 'ping':
      url += f'/{self.dev_id}/{self.create_signature(method_name)}'
      if method_name.lower() != 'createsession' and self.session_id:
        url += f'/{self.session_id}'
      url += f'/{self.create_timestamp()}'
      if params:
        if isinstance(params, (list, tuple)):
          params = '/'.join(fix_param(params))
        else:
          params = fix_param(params)
        url += f'/{params}'
    return url

  def create_timestamp(self, format_='%Y%m%d%H%M'):
    return f'{datetime.utcnow().strftime(format_)}00'

  def create_signature(self, method_name, format_='%Y%m%d%H%M'):
    return md5(f'{self.dev_id}{method_name.lower()}{self.auth_key}{self.create_timestamp(format_)}'.encode('utf-8')).hexdigest()
