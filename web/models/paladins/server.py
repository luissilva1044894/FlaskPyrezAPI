
from web.models import db

class PatchNote(db.Model):
	__tablename__ = 'patch_note'
	__bind_key__ = 'database'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	author = db.Column(db.String(40), nullable=True)
	content = db.Column(db.String(40), nullable=True)
	image_header = db.Column(db.Text, nullable=True)
	image_thumb = db.Column(db.Text, nullable=True)
	timestamp = db.Column(db.String(40), nullable=True)
	title = db.Column(db.Text, nullable=True)

	def __init__(self, author, content, image_header, image_thumb, timestamp, title):
		from utils import format_timestamp
		self.author = author
		self.content = content
		self.image_header = image_header
		self.image_thumb = image_thumb
		self.timestamp = format_timestamp(timestamp)
		self.title = title
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
			'image': { 'thumb': self.image_thumb, 'header': self.image_header },
			'timestamp': self.timestamp,
			'title': self.title
		}
class Platform(db.Model):
	__tablename__ = 'platform'
	__bind_key__ = 'database'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	name = db.Column(db.String(10), nullable=True)
	limited_access = db.Column(db.Boolean, nullable=True)
	online = db.Column(db.Boolean, nullable=True)
	version = db.Column(db.String(20), nullable=True)

	def __init__(self, name, limited_access, online, version):
		self.name = name
		self.limited_access = limited_access
		self.online = online
		self.version = version
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
			'name': self.name,
			'limited_access': self.limited_access,
			'online': self.online,
			'version': self.version
		}
class Server(db.Model):
	__tablename__ = 'server'
	__bind_key__ = 'database'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	created = db.Column(db.DateTime, nullable=True)
	game = db.Column(db.String(20), nullable=True)
	version = db.Column(db.String(20), nullable=True)
	api_version = db.Column(db.String(20), nullable=True)

	def __init__(self, game, version, api_version):
		from datetime import datetime
		self.created = datetime.utcnow()
		self.game = game
		self.version = version
		self.api_version = api_version
		self.save()
	def save(self):
		from sqlalchemy.exc import IntegrityError, InternalError, OperationalError, ProgrammingError
		try:
			for _ in Server.query.all():
				_.delete()
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
			'game': self.game,
			'version': self.version,
			'api_version': self.api_version,
			'platform': self.platform,
			'latest_patch_notes': self.patch_notes,
		}
	@property
	def platform(self):
		return [_.to_json() for _ in Platform.query.all()] or None
	@property
	def patch_notes(self):
		return [_.to_json() for _ in PatchNote.query.all()] or None
	@property
	def updated(self):
		from datetime import timedelta, datetime
		return datetime.utcnow() - self.created < timedelta(minutes=30)
