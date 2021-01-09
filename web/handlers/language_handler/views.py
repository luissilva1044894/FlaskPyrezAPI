#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
  g,
  request,
)

from utils.enums.language import get_language
from ...utils import create_blueprint

language_handler = create_blueprint(__name__)

@language_handler.app_context_processor
def utility_processor():
  def translate(message, lang=None, *, force=False, folder='lang'):
    return load_locate_json(message=message, lang=lang, force=force, folder=folder)
  return dict(translate=translate)

@language_handler.before_app_first_request
def before_app_first_request_handler():
  pass
  # carregar o arquivo json

@language_handler.before_app_request
def before_app_request_handler():
  # pegar idioma
  g.language = get_language(request)
