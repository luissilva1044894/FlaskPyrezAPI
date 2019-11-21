
from web.models import db

'''
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
		from utils import format_timestamp
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
			'image': { 'thumb': self.image_thumb, 'header': self.image_header },
			'timestamp': self.timestamp,
			'title': self.title
		}
'''
class Platform(db.Model):
	__tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
	__bind_key__ = __name__.split('.')[-2]

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
'''
class Server(db.Model):
	__tablename__ = __name__.split('.', 2)[-1].replace('.', '_')#'server'
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
	def to_json(self, lang=1, error_msg=None):
		return {
			'game': {
				'name': self.game,
				'version': self.version,
				'assets': {
					'cristal_images': 'https://app.box.com/s/orqsgij1kfyyo3co5gsg6k27ai9wab5d',
					'maps_images': 'https://app.box.com/s/rji72ijexal3mzl0mwfj3gimdoj5ii1i',
					'wallpapers': 'https://app.box.com/s/xshio67sqe7wxrse4tipaw3e3oipffnd',
					'champions_skins': 'https://app.box.com/s/qzi4jn7gu0upjspab78i6pn3fsw0vvrf'
				},
				'servers': self.platform,
				'latest_patch_notes': self.patch_notes(lang)
			},
			'version': self.api_version,
			'error_msg': error_msg
		}
	@property
	def platform(self):
		return [_.to_json() for _ in Platform.query.all()] or None
	def patch_notes(self, lang=1):
		#return [_.to_json() for _ in PatchNote.query.all()] or None
		return [_.to_json() for _ in PatchNote.query.filter_by(lang=lang)] or None
	@property
	def updated(self):
		from datetime import timedelta, datetime
		return datetime.utcnow() - self.created < timedelta(minutes=30)
'''
