#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError

class Session(db.Model):
  __tablename__ = 'session'
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  session_id = db.Column(db.String(50), unique=True, nullable=False)

  def __init__(self, session_id):
    self.session_id = session_id
    self.save()
  def save(self):
    try:
      for _ in Session.query.all():
        _.delete()
      db.session.add(self)
      db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
      db.session.rollback()
      self.save()
  def __repr__(self):
    return f'<{self.__class__.__name__} {self.to_json()}>'
  def __str__(self):
    return str(self.to_json())
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def to_json(self):
    return {f'{_}: {self.__dict__[_]}' for _ in self.__dict__ if not _.startswith('_')}
