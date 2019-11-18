#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BaseModel(db.Model):
    _index = db.Column('index', db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

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

from .player import PaladinsPlayer, SmitePlayer
from .session import Session
