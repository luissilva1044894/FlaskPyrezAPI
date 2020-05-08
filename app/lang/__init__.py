#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..utils import BaseEnumeration

class LanguageSupported(BaseEnumeration):
  English = 'en'
  Portuguese = 'pt'
  Spanish = 'es'
  Polish = 'pl'
  def __int__(self):
  	return {'es': 9, 'pl': 12, 'pt': 10}.get(str(self), 1)
  @property
  def lang_code(self):
    return {9: 'es_LA', 12: 'pl_PL', 10: 'pt_BR'}.get(int(self), 'en_US')
def get_accepted_languages(request_args):
  if request_args and hasattr(request_args, 'accept_languages'):
    return str(request_args.accept_languages).split('-')[0]
  return LanguageSupported.English#.value
def get_language(request_args):
  def get_lng(r):
    if hasattr(r, 'args'):
      r = r.args
    for _ in ['language', 'lang', 'lng']:
      __ = r.get(_)
      if __:
        return __
    return None
  aux = str(get_lng(request_args) or get_accepted_languages(request_args)).lower()
  try:
    return LanguageSupported(aux)#.value
  except ValueError:
    return LanguageSupported.English#.value
