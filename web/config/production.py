#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Config

class Production(Config):
  TESTING = DEVELOPMENT = DEBUG = False
  ENV = 'production'
  LOG_LEVEL = 'error'
  PREFERRED_URL_SCHEME = 'https'
