
from web.models import db

class ChampAbility(db.Model):
    __tablename__ = 'champ_alibity'
    __bind_key__ = 'database'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    damage_type = db.Column(db.String(10))
    recharge_seconds = db.Column(db.Integer)
