#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()
Base.query = db.session.query_property()

def init_db(app):
  # import all modules here that might define models so that
  # they will be registered properly on the metadata.
  # Otherwise you will have to import them first before calling init_db()
  app.logger.debug("Initializing Database Tables")
  Base.metadata.create_all(bind=db.engine)

def drop_db(app):
  app.logger.debug("Dropping Database Tables")
  Base.metadata.drop_all(bind=db.engine)
