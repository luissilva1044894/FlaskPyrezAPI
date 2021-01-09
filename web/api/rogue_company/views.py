#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  abort,
  g,
  render_template,
  request,
)
import requests

from utils.hirez import patch_notes
from ...utils import (
  create_blueprint,
  exceptions,
  get_page,
  decorators,
)
rogue_company = create_blueprint(__name__)

@rogue_company.before_request
def before_request_handler():
  pass

@rogue_company.errorhandler(requests.exceptions.ConnectionError)
@rogue_company.errorhandler(requests.exceptions.HTTPError)
def connection_error_handler(error=None):
  return '🚫 ERROR: An unexpected error has occurred!'

@rogue_company.errorhandler(404)
@rogue_company.route('/', methods=['GET'])
def root(error=None):
  """Homepage route."""
  return get_page(rogue_company)

@rogue_company.route('/patch_notes', methods=['GET'])
def _patch_notes_route_():
  """Get the latest Patch Notes"""
  return patch_notes.get_patch_notes(blueprint=rogue_company, lang=g.language, requested_json=g.requested_json, use_slug=True)
