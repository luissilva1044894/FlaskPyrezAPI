
# Flask-SQLAlchemy: Database
from flask_sqlalchemy import SQLAlchemy

def create_extesions():
  #https://github.com/nullcc/flask_api/blob/master/src/extensions.py#L26
  _extesions = {}

  _extesions['db'] = SQLAlchemy()

  return _extesions
