#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://github.com/dbuteau/games-matcher/blob/master/bot/models.py

import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, orm, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session, sessionmaker

from utils import slugify

class CustomBase(object):
  """https://github.com/lipowskm/game-deals-discord-bot/blob/8c321fb9f8204d53ceee4daef4b0a8b6c84b3b6b/database/base.py#L4"""
  @declared_attr
  def __tablename__(cls):
    _name_ = slugify(__name__.split('.', 2)[-1])
    if _name_.lower() == 'models':
      _name_ = slugify(cls.__name__)
    return _name_
  #if __name__.split('.')[-2] != 'web':
  #  print(__name__)
  #  @declared_attr
  #  def __bind_key__(cls):
  #    return __name__.split('.')[-2]

db = SQLAlchemy()
Base = declarative_base(cls=CustomBase)
Base.query = db.session.query_property()

class Database:
  """
  https://github.com/hhollenstain/autochannel-bot/blob/master/autochannel/data/models.py
  https://github.com/hhollenstain/autochannel-bot/blob/master/autochannel/data/database.py
  https://github.com/hhollenstain/autochannel-bot/blob/master/autochannel/lib/plugin.py
  """
  def __init__(self, uri=None):
    """Create an engine that stores data in the local directory's sqlalchemy_example.db file."""
    #path = os.path.abspath(__file__)
    self.engine = create_engine(uri or os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///app.db')
    #Base.metadata.bind = engine
    self.session = sessionmaker(bind=self.engine)()

  '''
  @property
  def session(self):
    Session = sessionmaker(bind=self.engine)
    return Session()
  '''

  def create_all(self):
    """Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL."""
    Base.metadata.create_all(bind=self.engine)

  def init(self):
    Base.metadata.create_all(self.engine)

  def init_db(app):
    """https://github.com/tritium01/udacity-capstone-rmg/blob/master/src/agency_models/models.py"""
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #db.app = app
    #db.init_app(app)
    #db.create_all()
    self.create_all()

  def drop_all(self):
    Base.metadata.drop_all(bind=self.engine)
    #os.rename('./peribot.db', './cogs/peribot.db')
    #moves database to correct folder for bot to function

db = Database()

from .paladins.player import Player
db.init()
print(db)
#try:
#  db.session.add(Player(id=1, name='abc', platform='dbc', discord_id=123))
#  db.session.commit()
#except:
#  print(e)
print(db.session.query(Player).all())

def init_db(app):
  # import all modules here that might define models so that
  # they will be registered properly on the metadata.
  # Otherwise you will have to import them first before calling init_db()
  app.logger.debug('Initializing Database Tables')
  Base.metadata.create_all(bind=db.engine)

def drop_db(app):
  app.logger.debug('Dropping Database Tables')
  Base.metadata.drop_all(bind=db.engine)

def get_engine(uri):
  #os.getenv('SQLALCHEMY_DATABASE_URI')
  return create_engine(uri)
  if uri:
    uri = f'sqlite:///database.sqlite'
  else:
    f'mysql+mysqlconnector://{mysql_cfg.username}:{mysql_cfg.password}@{mysql_cfg.address}:{mysql_cfg.port}/{mysql_cfg.database}'
  engine = create_engine(uri)
  return orm.scoped_session(orm.sessionmaker(bind=engine))

def get_session(engine=None):
  session = sessionmaker(bind=engine or db.engine)
  return session()

import enum
class Permissions(enum.Enum):
  banned = False
  default = None
  allowed = True

class Server(Base):
  #https://github.com/jcsumlin/Peribot/blob/master/create_databases.py#L11

  server_id = Column(Integer, primary_key=True, unique=True)
  server_name = Column(String)
  server_prefix = Column(String(32), nullable=True)
  server_region = Column(String)
  #owner_id = Column(Integer)
  #is_premium = Column(Boolean)

class UserPermissionsOfRoom(Base):
  __tablename__ = 'users_permissions_of_room'

  #server_id = Column(Integer, primary_key=True)
  server_id = Column(Integer, ForeignKey('servers.server_id'))
  owner_id = Column(Integer, primary_key=True)
  user_id = Column(Integer, primary_key=True)
  permissions = Column(Enum(Permissions), default=Permissions.default, nullable=False)


'''
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

from ..config import mysql_cfg

__all__ = ('Base', 'engine', 'session', 'DB_FILENAME', 'init_tables')

if mysql_cfg.enabled:
  try:
    import mysql.connector
  except (ImportError, ModuleNotFoundError):
    print('Could not find mysql connection library, please install it via pip:\n\tpip install --upgrade --user mysql-connector-python')
    input('\npress enter to exit...')
    exit(1)

Base = declarative_base()
DB_FILENAME = 'database.sqlite'
engine = create_engine(f'sqlite:///{DB_FILENAME}'
   if not mysql_cfg.enabled else
   f'mysql+mysqlconnector://{mysql_cfg.username}:{mysql_cfg.password}@{mysql_cfg.address}:{mysql_cfg.port}/{mysql_cfg.database}')
Session = orm.sessionmaker(bind=engine)
session = orm.scoped_session(Session)


from asyncio import Task

from sqlalchemy import Column, Integer, String, Float, Boolean

from .session import Base, init_tables
from ..config import cfg
from ..enums import CommandContext

__all__ = ('Quote', 'CustomCommand', 'Balance', 'CurrencyName', 'MessageTimer')


class Quote(Base):
  __tablename__ = 'quotes'

  id = Column(Integer, primary_key=True, nullable=False)
  user = Column(String(255))
  channel = Column(String(255), nullable=False)
  alias = Column(String(255))
  value = Column(String(255), nullable=False)

  @classmethod
  def create(cls, channel: str, value: str, user: str = None, alias: str = None):
    return Quote(channel=channel.lower(), user=user, value=value, alias=alias)


class CustomCommand(Base):
  __tablename__ = 'commands'

  id = Column(Integer, primary_key=True, nullable=False)
  name = Column(String(255), nullable=False)
  channel = Column(String(255), nullable=False)
  response = Column(String(255), nullable=False)
  context = CommandContext.CHANNEL
  permission = None

  @classmethod
  def create(cls, channel: str, name: str, response: str):
    return CustomCommand(channel=channel.lower(), name=name.lower(), response=response)

  @property
  def fullname(self):
    return self.name

  def __str__(self):
    return f'<CustomCommand channel={self.channel!r} name={self.name!r} response={self.response!r}>'


class Balance(Base):
  __tablename__ = 'balance'

  id = Column(Integer, nullable=False, primary_key=True)
  channel = Column(String(255), nullable=False)
  user = Column(String(255), nullable=False)
  balance = Column(Integer, nullable=False)

  @classmethod
  def create(cls, channel: str, user: str, balance: int = cfg.default_balance):
    return Balance(channel=channel.lower(), user=user, balance=balance)


class CurrencyName(Base):
  __tablename__ = 'currency_names'

  id = Column(Integer, nullable=False, primary_key=True)
  channel = Column(String(255), nullable=False)
  name = Column(String(255), nullable=False)

  @classmethod
  def create(cls, channel: str, name: str):
    return CurrencyName(channel=channel.lower(), name=name)


class MessageTimer(Base):
  __tablename__ = 'message_timers'

  id = Column(Integer, nullable=False, primary_key=True)
  name = Column(String(255), nullable=False)
  channel = Column(String(255), nullable=False)
  message = Column(String(255), nullable=False)
  interval = Column(Float, nullable=False)
  active = Column(Boolean, nullable=False, default=False)
  task: Task = None

  @property
  def running(self):
    return self.task is not None and not self.task.done()

  @classmethod
  def create(cls, channel: str, name: str, message: str, interval: float, active=False):
    return MessageTimer(name=name, channel=channel, message=message, interval=interval, active=active)


init_tables()


from typing import Union, Optional
from .models import Quote
from .session import session

__all__ = ('quote_exist', 'add_quote', 'get_quote', 'get_quote_by_alias', 'get_quote_by_id', 'delete_all_quotes',
  'delete_quote_by_alias', 'delete_quote_by_id')


def quote_exist(channel: str, id: int = None, alias: str = None) -> bool:
  """return if quote exist that has the same ID or ALIAS or both"""

  if id is None and alias is None:
    return False

  filters = [Quote.channel == channel]

  if id is not None:
    filters.append(Quote.id == id)
  if alias is not None:
    filters.append(Quote.alias == alias)

  return bool(session.query(Quote).filter(*filters).count())


def add_quote(quote: Quote) -> bool:
  """adds a quote to the quote DB, return a bool indicating if it was successful"""
  assert isinstance(quote, Quote), 'quote must of type Quote'

  if quote_exist(quote.channel, quote.id, quote.alias):
    return False

  session.add(quote)
  session.commit()
  return True


def get_quote_by_id(channel: str, id: int) -> Optional[Quote]:
  assert isinstance(id, int), 'quote_id must be of type int'
  return session.query(Quote).filter(Quote.id == id, Quote.channel == channel).one_or_none()


def get_quote_by_alias(channel: str, alias: str) -> Optional[Quote]:
  assert isinstance(alias, str), 'quote_alias must be of type str'
  return session.query(Quote).filter(Quote.alias == alias, Quote.channel == channel).one_or_none()


def get_quote(channel: str, id_or_alias: Union[str, int]) -> Optional[Quote]:
  """
  tries to find quote by parsing x to int first (uses value if its already a int),
  then tries to find quote using x as a alias
  returns the quote if one exist, else None
  """
  try:
    return get_quote_by_id(channel, int(id_or_alias))
  except ValueError:
    return get_quote_by_alias(channel, str(id_or_alias))


def delete_quote_by_id(channel: str, id: int) -> None:
  assert isinstance(id, int), 'quote_id must be of type int'
  session.query(Quote).filter(Quote.channel == channel, Quote.id == id).delete()
  session.commit()


def delete_quote_by_alias(channel: str, alias: str) -> None:
  assert isinstance(alias, str), 'quote_alias must be of type str'
  session.query(Quote).filter(Quote.channel == channel, Quote.alias == alias).delete()
  session.commit()


def delete_all_quotes():
  session.query(Quote).delete()
  session.commit()

class User(db.Model):
  bind_key = 'URL1'
  tablename = 'table1'
  table_args = {'extend_existing': True}

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(32), unique=True, nullable=False)

  def __init__(self, username = None):
    self.username = username

  def __repr__(self):
    return f'<Username {self.username}>'
'''