from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_apscheduler import APScheduler

db = SQLAlchemy()
jwt = JWTManager()
sendmail = Mail()
scheduler = APScheduler()