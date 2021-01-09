#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum as _enum

from utils import slugify

class Enum(_enum):
  def __str__(self):
    return str(self.value).lower()
  def __repr__(self):
    return self.__str__()
  def __eq__(self, other):
    if isinstance(other, (self.__class__, _enum)) or hasattr(other, '_value_'):
      return other._value_ == self._value_
    if isinstance(other, str):
      return slugify(other) == slugify(self._value_) or slugify(other) == slugify(self._name_)
    return self._value_ == other
  def get_name(self):
    return str(self.name)
  def get_id(self):
    _ = str(self.value)
    if _.isnumeric():
      return int(_)
    return _
  def __hash__(self):
    return hash(str(self.value).lower())
  def __int__(self):
    try:
      return int(self.get_id())
    except ValueError:
      pass
    return -1
  def upper(self):
    return str(self).upper()
  def lower(self):
    return str(self).lower()

"""
def print_exception(exc):
  print(' : '.join([str(_) for _ in [type(exc), exc.args, exc]]))


from flask import (
  Blueprint,
  g,
  request,
)

from ..utils import replace
from . import get_language

blueprint = Blueprint(replace(__name__, 'app.', 'api/', '.', replace_or_split=True), __name__)

'''
@blueprint.before_app_first_request
def before_app_first_request_():
  print('before_app_first_request')
'''
@blueprint.before_app_request
def before_app_request_():
  g._language_id_ = get_language(request)
  g._language_ = str(g._language_id_)

"""
