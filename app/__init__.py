#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://danidee10.github.io/2016/11/20/flask-by-example-8.html
#https://exploreflask.com/en/latest/blueprints.html
#https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/#internationalized-blueprint-urls
#https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/

#https://stackoverflow.com/questions/4239825/static-files-in-flask-robot-txt-sitemap-xml-mod-wsgi

import os

from .views import blueprint
from .utils import replace
from .utils.lib import import_from

def register(app):
  app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app', 'api')))

  os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
  for _mod in [_ for _ in os.listdir('.') if os.path.isdir(_) and not _ in ['lang', 'utils', 'migrations'] and not _.startswith('_')]:
    try:
      _lib = import_from(f'{__name__}.{_mod}')
      _lib.register(app)
    except (ModuleNotFoundError, AttributeError):
      print('>>> Failed to load:', f'{__name__}.{_mod}')
    else:
      print('>>> Blueprint loaded:', _lib.__name__ if hasattr(_lib, '__name__') else f'{__name__}.{_mod}')
