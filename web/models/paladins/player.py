#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .. import Base

class Player(Base):
  #__tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
  #__bind_key__ = __name__.split('.')[-2]

  id = Column(Integer, primary_key=True, autoincrement=False, nullable=False)
  name = Column(String(length=120), nullable=False)
  platform = Column(String(4), nullable=False)
  discord_id = Column(Integer, nullable=True)

  def __init__(self, id, name, platform, discord_id=None):
    self.id = id
    self.name = name
    self.platform = platform
    self.discord_id = discord_id
  
  def __repr__(self):
    return f'<{self.__class__.__name__} {self.to_dict()}>'
  
  def __str__(self):
    return str(self.to_dict())
  
  def to_dict(self):
    return {f'{_}: {self.__dict__[_]}' for _ in self.__dict__ if not _.startswith('_')}
