#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.exceptions import CustomException

class FieldRequired(CustomException):
  def __init__(self, f, *args, **kw):
    self.field = f
    super().__init__(f'Field “{f}” is required!')

class ChampRequired(CustomException):
  pass
class NoDeck(CustomException):
  pass
class NoChamp(CustomException):
  pass
class PlayerRequired(CustomException):
  pass
