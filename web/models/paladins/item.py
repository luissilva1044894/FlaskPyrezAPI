
from web.models import db, CRUD_Mixin

class Item(db.Model, CRUD_Mixin):
  __tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
  __bind_key__ = __name__.split('.')[-2]

  #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  item_id = db.Column(db.Integer)
  icon_id = db.Column(db.Integer)
  price = db.Column(db.Integer)
  item_type = db.Column(db.Integer)
  name = db.Column(db.Text)
  #name_english = db.Column(db.String(50))
  description = db.Column(db.Text)
  __lang__ = db.Column(db.Integer)

  def __init__(self, id=0, icon_id=0, price=0, item_type=0, name=None, name_english=None, description=None, lang=1):
    from boolify import boolify
    self.item_id = int(id)
    self.icon_id = int(icon_id)
    self.price = int(price)
    self.item_type = -1
    if item_type:
      from utils.paladins import get_item_type
      self.item_type = get_item_type(item_type.split(' ')[-2], True)
    self.name = name
    #self.name_english = name_english
    self.description = description.split(']', 1)[-1][1:]
    self.__lang__ = lang
    self.add()
