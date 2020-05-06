#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .views import blueprint
from ..utils import replace

def register(app):
  app.register_blueprint(blueprint, url_prefix='/{}'.format(replace(__name__, 'app.', 'api/')))
