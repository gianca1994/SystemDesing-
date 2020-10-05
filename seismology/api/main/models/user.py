from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(99), nullable=False)
    email = db.Column(db.String(99), nullable=False, unique=True, index=True)
    admin = db.Column(db.Boolean, nullable=False)
    sensors = db.relationship('Sensor', back_populates='user')

    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: %r %r %r >' % (self.id, self.email, self.admin)

