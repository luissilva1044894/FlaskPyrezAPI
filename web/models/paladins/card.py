
from web.models import db, CRUD_Mixin

class Card(db.Model, CRUD_Mixin):
  __tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
  __bind_key__ = __name__.split('.')[-2]

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  item_id = db.Column(db.Integer)
  icon_id = db.Column(db.Integer)
  card_id = db.Column(db.Integer)
  name = db.Column(db.Text)
  name_english = db.Column(db.Text)
  description = db.Column(db.Text)
  short_description = db.Column(db.Text)
  activation_schedule = db.Column(db.Boolean)
  lti = db.Column(db.Boolean)
  cooldown = db.Column(db.Integer)
  is_talent = db.Column(db.Boolean)
  scale = db.Column(db.Float)
  ability = db.Column(db.Text)
  __lang__ = db.Column(db.Integer)
  #champ_id = db.Column(db.Integer, db.ForeignKey(f'{__bind_key__}_champ.champ_id'))
  champ_id = db.Column(db.Integer)
  #Column(String(length=80))

  def __init__(self, id=0, icon_id=0, card_id=0, name=None, name_english=None, description=None, short_desc=None, actv_schedule=False, lti=False, cooldown=0, is_talent=False, lang=1, champ_id=None):
    from boolify import boolify
    from utils.paladins import extract_description, extract_scale
    self.item_id = int(id)
    self.icon_id = int(icon_id)
    self.card_id = int(card_id)
    self.name = name
    self.name_english = name_english#.replace('-', ' ')
    self.scale, description = extract_scale(description)
    self.is_talent = boolify(is_talent)
    self.description, self.ability = extract_description(description)
    self.short_description, _ = extract_description(short_desc)
    self.activation_schedule = boolify(actv_schedule)
    self.lti = boolify(lti)
    self.cooldown = int(cooldown)
    self.__lang__ = lang
    self.champ_id = -1
    if champ_id:
      self.champ_id = int(champ_id)
    self.add()
#https://docs.sqlalchemy.org/en/13/core/tutorial.html
'''
input(Card.__table__.insert().values(item_id=1, name='A'))
try:
  await database.execute(query)
except exc.IntegrityError:
  return JSONResponse({"message": "User already exists."})
return JSONResponse({"message": "Created user."})

try:
  for _ in Card.query.all():
    if _.__lang__ == 1:
      input(_.to_json())
except:
  pass
'''
