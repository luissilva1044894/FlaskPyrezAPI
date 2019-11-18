#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
db = SQLAlchemy()

class BaseModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	def save(self):
		try:
			db.session.add(self)
			db.session.commit()
		except (IntegrityError, InternalError, OperationalError, ProgrammingError):
			db.session.rollback()
	def delete(self):
		db.session.delete(self)
		db.session.commit()
