from marshmallow import validate
from marshmallow_sqlalchemy import SqlAS, Automaticfield
from main.models import UserModel

class User(SqlAS):
    class Meta:
        model = UserModel
        ordered = True
        instance = True
        relationships = True
    id = Automaticfield(dump_only=True)
    email = Automaticfield(required=True, validate=validate.Email())
    admin = Automaticfield(required=True)
