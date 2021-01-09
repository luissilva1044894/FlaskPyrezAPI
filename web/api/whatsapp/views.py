#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import os

from flask import (
  abort,
  Blueprint,
  current_app,
  g,
  jsonify,
  redirect,
  render_template,
  request,
)
from requests.exceptions import (
  ConnectionError,
  HTTPError,
)
from twilio.request_validator import RequestValidator
try:
  from twilio.twiml import Response
except ImportError:
  from twilio.twiml.messaging_response import MessagingResponse as Response

from ...utils import create_blueprint
from utils import environ

whatsapp = create_blueprint(__name__)
whatsapp.strict_slashes=False

def validate_twilio_request(f):
  @wraps(f)
  def decorated_function(*args, **kw):
    validator = RequestValidator(environ.get_env('TWILIO_AUTH_TOKEN', ''))

    request_valid = validator.validate(request.url, request.form, request.headers.get('X-TWILIO-SIGNATURE', ''))
    if request_valid or current_app.debug:
      return f(*args, **kw)
    return abort(403)
  return decorated_function

@whatsapp.errorhandler(404)
@whatsapp.route('/', methods=['GET'])
def root(error=None):
  return redirect(f"whatsapp://send?phone={environ.get_env('TWILIO_WHATSAPP_NUMBER')}&text=join {environ.get_env('TWILIO_JOIN_CODE')}")

@whatsapp.route('/status', methods=['POST', 'PUT'])
@validate_twilio_request
def incoming_status():
  print(request.form)
  return ''

@whatsapp.route('/message', methods=['POST', 'PUT'])
@validate_twilio_request
def incoming_message():
  def fix_param(param):
    if param and isinstance(param, (tuple, list)):
      return param[0]
    return param
  def fix_cmd(cmd):
    def fix_endpoint(arg=None):
      return {
        'overwatch': 'overwatch/',
        'smite': 'smite/',
        'twitch': 'twitch/',
        'youtube': 'youtube/',
      }.get(str(arg).lower(), '')
    return {
      'decks': 'decks', 'deck': 'decks',
      'lastmatch': 'last_match', 'last_match': 'last_match',
      'live_match': 'live_match', 'currentmatch': 'live_match', 'current_match': 'live_match', 'livematch': 'live_match', 'partida': 'live_match',
      'patch_notes': 'patch_notes',
      'stalk': 'stalk',
      'version': 'version',
      'kda': 'kda', 'winrate': 'kda',
    }.get(str(cmd).lower(), 'rank')

  resp = Response()

  msg, incoming_msg = resp.message(), request.form.get('Body')

  if incoming_msg:
    if str(incoming_msg)[0] == '!':
      incoming_msg = incoming_msg[1:]
    if hasattr(incoming_msg, 'split'):
      command, incoming_msg = incoming_msg.split(' ', 1)
      msg.body(get_url(f'https://nonsocial.herokuapp.com/api/{fix_cmd(command)}?query={incoming_msg}'))

  return resp.to_xml()
