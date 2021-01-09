#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boolify import boolify

from .. import is_hashable
from web.utils import fix_blueprint_name

def get_version(platform, api, blueprint, requested_json=False):
  def version(api):
    patch_info, server_status, = api.getPatchInfo(), api.getServerStatus()
    return {
      'patch_info': patch_info['version_string'] if is_hashable(patch_info) else None,
      'ret_msg': patch_info['ret_msg'] if is_hashable(patch_info) else None,
      'servers': [{y: x[y] for y in x} for x in (server_status if server_status and isinstance(server_status, list) else [])],
      #[{'operational' if 'status' in y else y: boolify(x[y]) if 'status' in y else x[y] for y in x} for x in (server_status if server_status and isinstance(server_status, list) else [])]
    }
  _v = version(api)
  if not requested_json:
    for _ in _v['servers']:
      if platform == _['platform']:
        return f"{fix_blueprint_name(blueprint).title()} is {_['status']} - {_v['patch_info']} ({_['version']})"
  #Paladins PC está OPERANTE - Versão atual: 3.3 (3.3.3661.5)
  return _v
