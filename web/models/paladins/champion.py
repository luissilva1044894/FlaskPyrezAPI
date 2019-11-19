
from web.models import db

class Champion(db.Model):
    __tablename__ = 'champion'
    __bind_key__ = 'database'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    weekly_rotation = db.Column(db.Boolean)
    health = db.Column(db.Integer)
    lore = db.Column(db.Text)
    title = db.Column(db.String(20))
    is_latest = db.Column(db.Boolean)
    #name_english

    @property
    def abilitys(self):
        return Ability.query.filter_by(champ_id=self.id).all()
