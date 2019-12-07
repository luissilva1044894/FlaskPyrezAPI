
from web.models import db

class PatchNote(db.Model):
	__tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
	__bind_key__ = 'database'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	author = db.Column(db.String(40), nullable=True)
	content = db.Column(db.Text, nullable=True)
	image_header = db.Column(db.Text, nullable=True)
	image_thumb = db.Column(db.Text, nullable=True)
	timestamp = db.Column(db.String(40), nullable=True)
	title = db.Column(db.Text, nullable=True)
	lang = db.Column(db.Integer, nullable=False)
	
	def __init__(self, author, content, image_header, image_thumb, timestamp, title, lang=1):
		from utils.time import format_timestamp
		self.author = author
		self.content = content
		self.image_header = image_header
		self.image_thumb = image_thumb
		self.timestamp = format_timestamp(timestamp)
		self.title = title
		self.lang = lang
		self.save()
	def save(self):
		from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
		try:
			db.session.add(self)
			db.session.commit()
		except (IntegrityError, InternalError, OperationalError, ProgrammingError):
			db.session.rollback()
			self.save()
	def delete(self):
		db.session.delete(self)
		db.session.commit()
	def __repr__(self):
		return '<{} {}>'.format(self.__class__.__name__, self.to_json())
	def __str__(self):
		return str(self.to_json())
	def to_json(self):
		return {
			'author': self.author,
			'content': self.content,
			'images': { 'thumb': self.image_thumb, 'header': self.image_header },
			'timestamp': self.timestamp,
			'title': self.title
		}
