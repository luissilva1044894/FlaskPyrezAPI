
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
class SmitePlayer(db.Model):
  __tablename__ = 'smite_players'
  __bind_key__ = 'smite'

  id = db.Column('player_id', db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=False)
  name = db.Column('player_name', db.String(120), nullable=False)
  platform = db.Column('player_platform', db.String(4), nullable=False)

  def __init__(self, id, name, platform):
    self.id = id
    self.name = name
    self.platform = platform
    self.save()
  def __repr__(self):
    return f'<SmitePlayer {self.name} (Id: {self.id} - Platform: {self.platform})>'
  def save(self):
    try:
      db.session.add(self)
      db.session.commit()
    except (IntegrityError, InternalError, OperationalError, ProgrammingError):
      db.session.rollback()
      _player = SmitePlayer.query.filter_by(id=self.id).first()
      _player.delete()
      self.save()
  def update(self, name):
    self.name = name
    db.session.commit()
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  def json(self):
    return { 'player_id': self.id, 'player_name': self.name, 'player_platform': self.platform }
