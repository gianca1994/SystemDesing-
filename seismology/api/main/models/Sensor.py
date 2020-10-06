from .. import db
from .user import User as UserModel


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(99), nullable=False)
    ip = db.Column(db.String(99), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', back_populates='sensors', uselist=False, single_parent=True)
    seisms = db.relationship('Seism', back_populates='sensor', passive_deletes='all')

    def __repr__(self):
        return '<Sensor: %r %r >' % (self.ip, self.name)


