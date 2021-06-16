from database import db


class PinColor(db.Model):
    __tablename__ = 'pincolor'
    color = db.Column(db.String, primary_key=True)
