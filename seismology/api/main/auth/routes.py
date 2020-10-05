from .. import db
from main.models import UserModel, SensorModel
from flask import request, Blueprint
from flask_jwt_extended import create_access_token


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    # Validamos si hay un email duplicado y alojamos en la variable user. Si hay un duplicado nos da error 404.
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get('email')).first_or_404()

    if user.validate_pass(request.get_json().get('password')):
        access_token = create_access_token(identity=user)
        data = '{"id":"' + str(user.id) + '","email":"' + str(user.email) + '","access_token":"' + access_token + '"}'
        return data, 200
    else:
        return 'Incorrect password', 401
