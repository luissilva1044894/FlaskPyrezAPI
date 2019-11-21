#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.models import db

class Paladins(db.Model):
  __tablename__ = 'paladins_player'
  __bind_key__ = 'paladins'#paladins_players

  id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
  name = db.Column(db.String(120), nullable=False)
  platform = db.Column(db.String(4), nullable=False)
  discord_id = db.Column(db.Integer, nullable=True)
  #_game = db.Column(db.String(8), primary_key=False, unique=False, nullable=True, autoincrement=False)

  def __init__(self, id, name, platform, discord_id=None):
    self.id = id
    self.name = name
    self.platform = platform
    self.discord_id = discord_id
    self.save()
  def save(self):
    from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
    try:
        db.session.add(self)
        db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
        db.session.rollback()
        getattr(self.__class__, 'query').filter_by(id=self.id).first().delete()
        self.save()
  def __repr__(self):
    return '<{} {}>'.format(self.__class__.__name__, self.to_json())
  def __str__(self):
    return str(self.to_json())
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def to_json(self):
    return {f'{_}: {self.__dict__[_]}' for _ in self.__dict__ if not _.startswith('_')}

class Smite(db.Model):
  __tablename__ = 'smite_player'
  __bind_key__ = 'smite'

  id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
  name = db.Column(db.String(120), nullable=False)
  platform = db.Column(db.String(4), nullable=False)
  discord_id = db.Column(db.Integer, nullable=True)

  def __init__(self, id, name, platform):
    self.id = id
    self.name = name
    self.platform = platform
    self.save()
  def save(self):
    from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
    try:
        db.session.add(self)
        db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
        db.session.rollback()
        getattr(self.__class__, 'query').filter_by(id=self.id).first().delete()
        self.save()
  def __repr__(self):
    return '<{} {}>'.format(self.__class__.__name__, self.to_json())
  def __str__(self):
    return str(self.to_json())
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def to_json(self):
    return {f'{_}: {self.__dict__[_]}' for _ in self.__dict__ if not _.startswith('_')}
