#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Config

class Developement(Config):
  DEVELOPMENT, ENV = True, 'development'
  LOG_LEVEL = 'debug'
