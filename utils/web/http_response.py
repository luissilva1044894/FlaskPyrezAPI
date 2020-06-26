#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Response

def HttpResponse(resp, status, mimetype='application/json', **kw):
  return Response(json.dumps(resp), status=status, mimetype=mimetype, **kw)

def OkResponse(resp):
  resp.update({'success': True})
  return HttpResponse(resp, 200)

def NotOkResponse(resp):
  resp.update({'success': False})
  return HttpResponse(resp, 400)
