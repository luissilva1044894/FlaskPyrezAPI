#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from utils.web import create_blueprint

context_processor = create_blueprint(__name__)

@context_processor.app_context_processor
def utility_processor():
  return { 'current_year': datetime.utcnow().year }
  #def translate(message, lang=None, *, force=False, folder='lang'):
  #  return load_locate_json(message=message, lang=lang, force=force, folder=folder)
  #return dict(current_time=datetime.now(), current_year=datetime.utcnow().year, translate=translate)

