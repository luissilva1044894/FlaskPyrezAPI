#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
class Session(db.Model):
  __tablename__ = 'session'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  session_id = db.Column(db.String(50))#, unique=True, nullable=False
  def __init__(self, session_id):
    self.session_id = session_id
    self.save()
  def __repr__(self):
    return f'<Session {self.session_id}>'
  def save(self):
    try:
      for sess in Session.query.all():
        sess.delete()
      db.session.add(self)
      db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
      db.session.rollback()
  def update(self, name):
    self.name = name
    db.session.commit()
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def json(self):
    return { 'session_id': self.session_id }
