from flask_restful import Resource
from flask import request, jsonify
from api.main import db
from main.models import SeismModel, SensorModel
from random import randint, uniform
import time
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow_sqlalchemy import SqlAS, Automaticfield, Field
from main.models import SeismModel
from main.mapping import SensorSchema


class Seism(SqlAS):
    class Meta:
        model = SeismModel
        ordered = True
        instance = True
        relationships = True
    id = Automaticfield(dump_only=True)  # Read from db only
    datime = Automaticfield(format="%Y-%m-%d %H:%M:%S", required=True)
    depth = Automaticfield(required=True)
    magnitude = Automaticfield(required=True)
    latitude = Automaticfield(required=True)
    longitude = Automaticfield(required=True)
    verified = Automaticfield(required=True)
    sensorId = Automaticfield(required=True, load_only=True)
    sensor = Field.Nested(SensorSchema, dump_only=True)  # Read from db only
