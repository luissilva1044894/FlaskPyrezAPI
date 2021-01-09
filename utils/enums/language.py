#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .__init__ import Enum

class Language(Enum):
  English = 'en'
  Portuguese = 'pt'
  Spanish = 'es'
  Polish = 'pl'

  def __int__(self):
    return {'es': 9, 'pl': 12, 'pt': 10}.get(self.value, 1)

  def __str__(self):
    return {9: 'es', 10: 'pt', 12: 'pl'}.get(int(self), 'en')

  @property
  def lang_code(self):
    return {9: 'es_LA', 12: 'pl_PL', 10: 'pt_BR'}.get(int(self), 'en_US')

  @property
  def supported(self):
    return self in [Language.English, Language.Portuguese, Language.Spanish, Language.Polish]

def get_accepted_languages(args):
  if args and hasattr(args, 'accept_languages'):
    return str(args.accept_languages).split('-')[0]
  return Language.English

def get_language(args):
  def fix_language(v):
    return {'9': 'es', '10': 'pt', '12': 'pl'}.get(str(v).lower(), v)
  def get_lng(r):
    if hasattr(r, 'args'):
      r = r.args
    if hasattr(r, 'get'):
      for _ in ['language', 'lang', 'lng']:
        __ = r.get(_)
        if __:
          return fix_language(__)
    return None
  try:
    return Language(get_lng(args) or get_accepted_languages(args))
  except (TypeError, ValueError):
    return Language.English
