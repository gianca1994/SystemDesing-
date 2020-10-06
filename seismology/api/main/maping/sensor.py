from flask_restful import Resource
from flask import request, jsonify
from api.main import db
from ..maping import UserSchema
from ..models import SensorModel
from main.auth.decorators import admin_required
from marshmallow_sqlalchemy import SqlAS, Automaticfield, Field


class Sensor(SqlAS):
    class Meta:
        model = SensorModel
        ordered = True
        instance = True
        relationships = True
    id = Automaticfield(dump_only=True)
    name = Automaticfield(required=True)
    active = Automaticfield(required=True)
    ip = Automaticfield(required=True)
    port = Automaticfield(required=True)
    status = Automaticfield(required=True)
    userId = Automaticfield(required=True, load_only=True)
    user = Field.Nested(UserSchema, dump_only=True)
