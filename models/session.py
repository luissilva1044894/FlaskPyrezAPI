
from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError

from . import db

class Session(db.Model):
  __tablename__ = 'session'
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  session_id = db.Column(db.String(50), unique=True, nullable=False)

  @staticmethod
  def get_session_id():
    try:
      last_session = Session.query.first()
    except (OperationalError, ProgrammingError):
      last_session = None
    else:
      last_session = last_session.session_id or None
    return last_session

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
