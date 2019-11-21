#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class CRUD_Mixin(object):
  #__bind_key__ = 'database'
  #__abstract__ = True
  id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)

  def add(self, resource=None):
  	db.session.add(resource or self)
  	return db.session.commit()
  def update(self):
  	return db.session.commit()
  def delete(self, resource=None):
    db.session.delete(resource or self)
    return db.session.commit()
  def save(self):
    '''
  	from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
  	try:
  		self.add()
  	except (IntegrityError, InternalError, OperationalError, ProgrammingError):
  		db.session.rollback()
  		getattr(self.__class__, 'query').filter_by(id=self.id).first().delete()
  		self.save()
    '''
    self.add()
  def __repr__(self):
  	return '<{} {}>'.format(self.__class__.__name__, self.to_json())
  def __str__(self):
  	return str(self.to_json())
  def to_json(self):
  	#return {c.name: getattr(self, c.name) for c in self.__table__.columns}
  	return {_: self.__dict__[_] for _ in self.__dict__ if not _.startswith('_')}

from .player import Paladins, Smite
from .session import Session
from .paladins.server import Server
from .paladins.platform import Platform
from .paladins.patch_note import PatchNote
from .paladins import champ
#, ChampInfo, Ability, AbilityInfo
