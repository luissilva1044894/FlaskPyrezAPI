
from web.models import db

class Skin(db.Model):
    __tablename__ = 'champ_skin'
    __bind_key__ = 'database'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_2 = db.Column(db.Integer)
    name = db.Column(db.String(20))
    rarity = db.Column(db.String(20))

    @property
    def abilitys(self):
        return Ability.query.filter_by(champ_id=self.id).all()
