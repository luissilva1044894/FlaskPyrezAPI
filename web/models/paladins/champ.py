
from web.models import db, CRUD_Mixin
class Champ(db.Model, CRUD_Mixin):
  __tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
  __bind_key__ = __name__.split('.')[-2]

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  champ_id = db.Column(db.Integer)#, nullable=False, unique=False)
  name = db.Column(db.Text)
  name_english = db.Column(db.Text)
  free_rotation = db.Column(db.Boolean)
  weekly_rotation = db.Column(db.Boolean)
  health = db.Column(db.Integer)
  is_latest = db.Column(db.Boolean)
  patreon = db.Column(db.Text)
  lore = db.Column(db.Text)
  title = db.Column(db.Text)
  role = db.Column(db.Text)
  __lang__ = db.Column(db.Integer, unique=False)
  #__version__ = db.Column(db.String(20), nullable=True)
  
  #from sqlalchemy.orm import backref, relation
  #from .champ_ability import Ability
  #abilitys = relation(Ability, backref=backref(__tablename__, lazy=True))#db.relationship('Ability', backref=__tablename__, lazy='dynamic')
  #abilitys = db.relationship('Ability', backref=__tablename__, lazy=True)
  #https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/?highlight=backref
  #https://github.com/pallets/flask-website/blob/master/flask_website/utils.py
  #lazy=[True, 'select', 'immediate', 'joined', 'selectin'][0]
  #Async SQLAlchemy: https://github.com/aio-libs/aiohttp_admin/blob/master/demos/blog/aiohttpdemo_blog/generate_data.py#L37-L43

  def __init__(self, champ_id, name, free_rotation=False, weekly_rotation=False, health=0, is_latest=False, name_english=None, patreon=None, lore=None, title=None, role=None, lang=1, abilitys=None):
    from boolify import boolify
    self.champ_id = int(champ_id)
    self.name = name
    self.free_rotation = boolify(free_rotation)
    self.weekly_rotation = boolify(weekly_rotation)
    self.health = int(health)
    self.is_latest = boolify(is_latest)
    self.name_english = name_english
    self.patreon = patreon
    self.lore = lore
    self.title = title
    self.role = role.split(' ', 1)[-1]
    self.__lang__ = int(lang)
    if abilitys:
      self.abilitys = abilitys
    self.add()
  def add_ability(self, a):
    self.abilitys.append(a)
  @staticmethod
  def get(lang=None):
    return Champ.filter_by(__lang__=lang or 1)
  @property
  def cards(self, lang=None):
    from .card import Card
    __cards__ = [_ for _ in Card.query.all() if _.champ_id == self.champ_id or (lang and _.__lang__ == lang and _.champ_id == self.champ_id)]
    __cards__.sort(key=lambda k: k.ability)
    return __cards__
  
  @staticmethod
  def update(_api, langs=[1, 2, 3, 9, 10, 11, 12, 13]):
    from utils import get_url
    from .item import Item
    from .card import Card
    from .ability import Ability
    #from .server import Server
    #_server = Server.get(_api)
    [ _.delete() for _ in Ability.query.all()]
    [ _.delete() for _ in Card.query.all()]
    [ _.delete() for _ in Item.query.all()]
    for l in langs:
      i = _api.getItems(l)
      for ig in [_ for _ in i if _['champion_id'] == 0]:
        Item(id=ig.itemId, icon_id=ig.iconId, price=ig.itemPrice, item_type=ig.itemType, name=ig.deviceName, name_english=None, description=ig.itemDescription, lang=l)
      for g in _api.getGods(l):
        __js0n__ = get_url('https://cms.paladins.com/wp-json/wp/v2/champions?slug={}&lang_id={}'.format(g['Name_English'], l))
        __js0n__ = __js0n__[0] if __js0n__ and len(__js0n__) > 0 else {}
        if l == langs[0]:
          Champ(champ_id=g.godId, name=g.godName, free_rotation=g.onFreeRotation, weekly_rotation=g.onFreeWeeklyRotation, health=g.health, is_latest=g.latestGod, name_english=g['Name_English'], patreon=g.pantheon, lore=g.lore, title=g.title, role=g.roles, lang=l)
        for ch_cards in [_ for _ in i if _['champion_id'] == int(g.godId) and not (_['item_type'].lower().rfind('deprecated')!= -1 or _['item_type'].lower().rfind('default')!= -1)]:
          card_id, name_english, actv_schedule, lti = 0, None, False, False
          for c in __js0n__.get('cards', {}):
            if c.get('card_id2', 0) == ch_cards.itemId:
              card_id = c.get('card_id1')
              name_english = c.get('card_name_english')
              actv_schedule = c.get('active_flag_activation_schedule')
              lti = c.get('active_flag_lti')
          Card(id=ch_cards.itemId, icon_id=ch_cards.iconId, card_id=card_id, name=ch_cards.deviceName, name_english=name_english, description=ch_cards['Description'], short_desc=ch_cards['ShortDesc'], actv_schedule=actv_schedule, lti=lti, cooldown=ch_cards['recharge_seconds'], is_talent=ch_cards['item_type'].lower().rfind('talent') != -1, lang=l, champ_id=g.godId)
        for ab in g.abilitys:
          #ab_vid, time = None, None
          #for ab_vid in __js0n__.get('cards', {}):
            #if ab[-2:] == b[-2:]:
            Ability(ability_id=ab.id, damage_type=ab.damageType, cooldown=ab.rechargeSeconds, description=ab.description, summary=ab.summary, lang=l, champ_id=g.godId)
      db.session.commit()
