
from web.models import db, CRUD_Mixin

class Ability(db.Model, CRUD_Mixin):
	__tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
	__bind_key__ = __name__.split('.')[-2]
	print(__tablename__)

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	ability_id = db.Column(db.Integer)
	#damage_type = db.Column(db.Integer)
	ability = db.Column(db.Text)
	description = db.Column(db.Text)
	damage_type = db.Column(db.Integer)
	summary = db.Column(db.Text)
	cooldown = db.Column(db.Integer)
	__lang__ = db.Column(db.Integer)
	champ_id = db.Column(db.Integer, db.ForeignKey(f'{__bind_key__}_champ.champ_id'))

	def __init__(self, ability_id, damage_type=0, cooldown=0, description=None, summary=None, lang=1, champ_id=None):
		from utils.paladins import get_dmg_type
		import re
		self.ability_id = int(ability_id)
		self.damage_type = get_dmg_type(damage_type, True)
		self.cooldown = int(cooldown)
		self.ability = None
		match = re.compile(r'\[(.+?)\] (.*)').match(description)
		if match:
			self.ability = match.group(1)
			description = match.group(2).strip()
		self.description = description
		self.summary = summary
		self.__lang__ = int(lang)
		if champ_id:
			self.champ_id = int(champ_id)
		self.save()
	
