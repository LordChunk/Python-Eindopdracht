from database import db
from models.Color import Color


class PinColor(db.Model):
    __tablename__ = 'pincolor'
    color = db.Column(db.String, primary_key=True)

    @staticmethod
    def seed():
        if PinColor.query.count() != len(Color):
            PinColor.query.delete()
            for c in Color:
                db.session.add(PinColor(color=str(c)))
            db.session.commit()
