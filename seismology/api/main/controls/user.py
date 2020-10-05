from flask_restful import Resource
from flask import request, jsonify
from ..auth.decorators import admin_required
from ..mapping import UserSchema
from ..repository import UserRepository
from ..resources import existing_email


UserSchema = UserSchema()

class User(Resource):

    @admin_required
    def get(self, id):
        userR = UserRepository()
        userR.set_id(id)
        return UserSchema.dump(userR.get_or_404())

    @admin_required
    def put(self, id):
        userR = UserRepository()
        userR.set_id(id)
        user = userR.get_or_404()
        userR.set_instance(user)
        json = request.get_json().items()
        userR.set_input_json(json=json)
        return userR.modify()

    @admin_required
    def delete(self, id):
        userR = UserRepository()
        userR.set_id(id)
        user = userR.get_or_404()
        userR.set_instance(instance=user)
        return userR.delete()

class Users(Resource):

    @admin_required
    def get(self):
        userR = UserRepository()
        jsonItems = request.get_json().items()
        userR.set_input_json(json=jsonItems)
        return userR.get_all()

    @admin_required
    def post(self):
        userR = UserRepository()
        json = request.get_json()
        existing_email(json["email"])
        userR.set_addition_json(json=json)
        return userR.add()
