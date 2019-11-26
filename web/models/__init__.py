#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class CRUD_Mixin(object):
  @classmethod
  def create(cls, **kwargs):
    instance = cls(**kwargs)
    return instance.save()
  #__bind_key__ = 'database'
  #__abstract__ = True
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  def add(self, resource=None):
    """Saves the object to the database."""
    '''
    from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
    try:
      self.add()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
      db.session.rollback()
      getattr(self.__class__, 'query').filter_by(id=self.id).first().delete()
      self.save()
    '''
    db.session.add(resource or self)
    #db.session.commit()
    return self
  def save(self, resource=None):
    return self.save(resource)
  def append(self, attr, resource):
    getattr(self, attr).append(resource)
  def commit(self):
    return db.session.commit()
  def update(self):
  	return db.session.commit()
  def delete(self, resource=None):
    """Delete the object from the database."""
    db.session.delete(resource or self)
    return self
  def __repr__(self):
  	return '<{} {}>'.format(self.__class__.__name__, self.to_json())
  def __str__(self):
  	return str(self.to_json())
  def to_json(self):
  	#return {c.name: getattr(self, c.name) for c in self.__table__.columns}
  	return {_: self.__dict__[_] for _ in self.__dict__ if not _.startswith('_')}#and not _ == 'id'
