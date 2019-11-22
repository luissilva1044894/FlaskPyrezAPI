
from web.models import db, CRUD_Mixin

class Card(db.Model, CRUD_Mixin):
  __tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
  __bind_key__ = __name__.split('.')[-2]
  print(__tablename__)

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  item_id = db.Column(db.Integer)
  icon_id = db.Column(db.Integer)
  card_id = db.Column(db.Integer)
  name = db.Column(db.String(50))
  name_english = db.Column(db.String(50))
  description = db.Column(db.Text)
  short_description = db.Column(db.Text)
  activation_schedule = db.Column(db.Boolean)
  lti = db.Column(db.Boolean)
  cooldown = db.Column(db.Integer)
  is_talent = db.Column(db.Boolean)
  scale = db.Column(db.Float)
  ability = db.Column(db.String(50))
  __lang__ = db.Column(db.Integer)
  champ_id = db.Column(db.Integer, db.ForeignKey(f'{__bind_key__}_champ.champ_id'))

  def __init__(self, id=0, icon_id=0, card_id=0, name=None, name_english=None, description=None, short_desc=None, actv_schedule=False, lti=False, cooldown=0, is_talent=False, lang=1, champ_id=None):
    from boolify import boolify
    self.item_id = int(id)
    self.icon_id = int(icon_id)
    self.card_id = int(card_id)
    self.name = name
    self.name_english = name_english
    self.scale = 0
    import re
    scale = re.search('=(.+?)\|', description)
    try:
      self.scale = float(str(scale.group(1)).replace(',', '.'))
      # if scale % 2 == 0 or scale % 2 == scale: scale = int(scale)
    except AttributeError:
      pass
    try:
      description = description.replace('{' + str(re.search('{(.*?)}', description).group(1)) + '}', '{SCALE}')
    except AttributeError:
      pass
    #desc = re.sub('[\[].*?[\]] ', '', desc)
    self.ability = None
    match = re.compile(r'\[(.+?)\] (.*)').match(description)
    if match:
      self.ability = match.group(1)
      description = match.group(2).strip()
    self.is_talent = boolify(is_talent)
    self.description = description
    match = re.compile(r'\[(.+?)\] (.*)').match(short_desc)
    if match:
      short_desc = match.group(2).strip()
    self.short_description = short_desc
    self.activation_schedule = boolify(actv_schedule)
    self.lti = boolify(lti)
    self.cooldown = int(cooldown)
    self.__lang__ = lang
    if champ_id:
      self.champ_id = int(champ_id)
    self.save()
