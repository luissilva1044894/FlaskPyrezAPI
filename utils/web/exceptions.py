#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FieldRequired(Exception):
  def __init__(self, f, *args, **kw):
    self.field = f
    super().__init__(f'Field “{f}” is required!')
