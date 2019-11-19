
from web.models import db

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
		self.game = game or __name__.split('.')[-2]
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
		from utils.file import read_file
		__links__ = read_file('data/links.json', is_json=True)
	
		return {
			'game': {
				'name': self.game,
				'version': self.version,
				'links': __links__.get(self.game, ''),
				'servers': self.platform,
				'latest_patch_notes': self.patch_notes(lang)
			},
			'version': self.api_version,
			'error_msg': error_msg
		}
	@property
	def platform(self):
		from .platform import Platform
		return [_.to_json() for _ in Platform.query.all()] or None
	def patch_notes(self, lang=1):
		from .patch_note import PatchNote
		#return [_.to_json() for _ in PatchNote.query.all()] or None
		return [_.to_json() for _ in PatchNote.query.filter_by(lang=lang)] or None
	@property
	def updated(self):
		from datetime import timedelta, datetime
		return datetime.utcnow() - self.created < timedelta(minutes=30)
