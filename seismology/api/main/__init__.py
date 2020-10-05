import os
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from .controls import UserC, UsersC
from .controls import UnverifSeismC, UnverifSeismsC
from .controls import VerifSeismC, VerifSeismsC
from .controls import SensorC, SensorsC
from .auth.routes import auth
from .extensions import db, jwt, sendmail, scheduler

api = Api()
load_dotenv()

DataBase_Path = str(os.getenv("SQLALCHEMY_DB_PATH"))
DataBase_Name = str(os.getenv("SQLALCHEMY_DB_NAME"))
DataBase_Url = "sqlite:////" + DataBase_Path + DataBase_Name
Sql_TrackModif = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
JWT_SecretKey = os.getenv("JWT_SECRET_KEY")
JWT_TokenExpires = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))


def PrimaryKeys(conection, _conection_record):
    conection.execute('pragma foreign_keys=ON')


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config())

    if not os.path.exists(DataBase_Path + DataBase_Name):
        os.mknod(DataBase_Path + DataBase_Name)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Sql_TrackModif
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + DataBase_Url
    db.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    app.config["JWT_SECRET_KEY"] = JWT_SecretKey
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_TokenExpires
    jwt.init_app(app)

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["FLASKY_MAIL_SENDER"] = os.getenv("FLASKY_MAIL_SENDER")
    sendmail.init_app(app)

    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', PrimaryKeys)

    api.add_resource(UserC, '/user/<id>')
    api.add_resource(UsersC, '/users')
    api.add_resource(SensorC, '/sensors/<id>')
    api.add_resource(SensorsC, '/sensors')
    api.add_resource(VerifSeismC, '/verif-seisms/<id>')
    api.add_resource(VerifSeismsC, '/verif-seisms')
    api.add_resource(UnverifSeismC, '/unverif-seisms/<id>')
    api.add_resource(UnverifSeismsC, '/unverif-seisms')
    app.register_blueprint(auth.routes.auth)

    api.init_app(app)
    return app
