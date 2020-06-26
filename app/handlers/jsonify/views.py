#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
import json

from flask import request, current_app as app

from utils.web import (
  requested_json,
  create_blueprint,
)

jsonify = create_blueprint(__name__)

@jsonify.after_app_request
def jsonify_func(resp):
  if requested_json(resp):
    _indent_, separators = None, (',', ':')
    if request.args.get('format', 'json') in ['json_pretty', 'pretty'] or app.config['JSONIFY_PRETTYPRINT_REGULAR']:
      _indent_, separators = 2, (',', ': ')
    resp.set_data(json.dumps(resp.get_json(), sort_keys=app.config['JSON_SORT_KEYS'], ensure_ascii=app.config['JSON_AS_ASCII'], indent=_indent_, separators=(',', ':')))
    resp.headers['Cache-Control'] = 'public, max-age=300'
    resp.headers['Expires'] = format_datetime((datetime.utcnow() + timedelta(seconds=300)).replace(tzinfo=timezone.utc), usegmt=True)
  return resp
