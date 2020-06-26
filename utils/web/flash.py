#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import flash
from bs4 import BeautifulSoup

def flash_msg(message, category='default'):
  """For the given message, if html is present, add bootstrap .alert-link class to all links"""
  if message.startswith('<p>') and message.endswith('</p>'):
    msg = BeautifulSoup(message, 'lxml')
    for a in msg.find_all('a'):
      if not a.get('class'):
        a.attrs.update({'class': []})
      a['class'].extend(['alert-link'])
    msg = str(msg)

  flash(msg, category)

def danger(msg):
  flash_msg(msg, category='danger')

def warning(msg):
  flash_msg(msg, category='warning')

def info(msg):
  flash_msg(msg, category='info')

def success(msg):
  flash_msg(msg, category='success')

__all__ = [
  'danger',
  'info',
  'success',
  'warning',
]