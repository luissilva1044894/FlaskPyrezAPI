#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
from functools import wraps, partial
import importlib
import os

from flask import Blueprint, current_app, g, request, jsonify, url_for

from utils import is_hashable

def fix_blueprint_name(blueprint):
  if hasattr(blueprint, 'name'):
    name = blueprint.name.split('.')
    if len(name) > 1:
      return name[1]
    return name[-1]
  return blueprint

def get_page(blueprint):
  if requested_json(request):
    return auto_doc(blueprint)
  return ' '.join([blueprint.name, request.url_rule.rule])

def auto_doc(blueprint=None, include_static=False):
  def has_no_empty_params(rule):
    if hasattr(rule, 'arguments'):
      return len(rule.defaults or ()) >= len(rule.arguments or ())
    return True
  def get_doc(rule):
    if hasattr(current_app.view_functions[rule.endpoint], 'import_name'):
      return {rule.rule: '%s\n%s' % (','.join(list(rule.methods)), import_string(current_app.view_functions[rule.endpoint].import_name).__doc__)}
    return current_app.view_functions[rule.endpoint].__doc__
  def url_for_rule(r):
    try:
      if hasattr(r, 'arguments'):
        return url_for(r.endpoint, **dict(f'[{_}]' for _ in r.arguments))
      return url_for(r.endpoint)
    except (ValueError, TypeError):
      pass
    return '/'
  return jsonify({
    'namespace': blueprint.name.split('.')[0] if hasattr(blueprint, 'name') else current_app.name,
    'routes': {
    url_for_rule(r): {
      'methods': ', '.join(sorted(r.methods)), #'methods': sorted(r.methods)
      'description': get_doc(r),
      'slashes': r.strict_slashes} for r in current_app.url_map.iter_rules() if 'GET' in r.methods and has_no_empty_params(r) and (hasattr(blueprint, 'url_prefix') and blueprint.url_prefix in r.rule)#(blueprint and 'api' not in r.rule) or
    },
    '_links': {'up': [request.base_url[:request.base_url.rfind(blueprint.name.split('.')[0] if hasattr(blueprint, 'name') else current_app.name)]]}
  })

def get_value(field, req=None, default=None):
  if not req:
    req = request
  if req and field:
    '''
    print(g.__dict__)
    if hasattr(g, field):
      _ = getattr(g, field, None)
      if _:
        return _
    '''
    if isinstance(field, (list, tuple)):
      for f in field:
        _ = get_value(f, req)
        if _:
          return _
      return None
    if hasattr(req, 'is_json') and req.is_json:
      _ = req.get_json(force=True, silent=True, cache=True)
      if _ and field in _:
        return _[field]
    if hasattr(req, 'headers') and field in req.headers:
      _ = req.headers.get(field)
      if _:
        return _
    if hasattr(req, 'args'):
      req = req.args
    if hasattr(req, 'form'):
      req = req.form
    if is_hashable(req) and field in req and req[field]:
      return req[field]#args.get(field) or default
  return default

def create_blueprint(name, import_name=None, *, package=None, url_prefix=None, static_url_path=None, **options):
  if name and not import_name:
    _name = name if isinstance(name, (list, tuple)) else name.split('.')[1:]
    url_prefix = url_prefix or '/{}'.format('/'.join(_name[:-1]))
    import_name = name
    name = '.'.join(_name)
    static_url_path = static_url_path or ''
  try:
    module = importlib.import_module(package)
  except (ImportError, AttributeError) as e:
    return create_blueprint(name=name, import_name=import_name, package=package or 'flask', url_prefix=url_prefix, static_url_path=static_url_path, **options)
  return module.Blueprint(name, import_name, url_prefix=url_prefix, static_url_path=static_url_path, **options)

def requested_json(arg):
  return (hasattr(arg, 'args') and 'json' in arg.args.get('json', arg.args.get('format', '')).lower()) or (hasattr(arg, 'accept_mimetypes') and arg.accept_mimetypes.accept_json and not arg.accept_mimetypes.accept_html) or hasattr(arg, 'headers') and arg.headers.get('Content-Type', '').lower() == current_app.config.get('JSONIFY_MIMETYPE', '').lower()
