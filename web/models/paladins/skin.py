
from web.models import db

class Skin(db.Model):
    __tablename__ = __name__.split('.', 2)[-1].replace('.', '_')
    __bind_key__ = __name__.split('.')[-2]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_2 = db.Column(db.Integer)
    name = db.Column(db.String(20))
    rarity = db.Column(db.String(20))

    @property
    def abilitys(self):
        return Ability.query.filter_by(champ_id=self.id).all()
