from ..models import UserModel, SeismModel
from ..extensions import db

def User_Exists(id):
    user = db.session.query(UserModel).filter(UserModel.id == id).scalar() is not None
    if user:
        return True
    else:
        return False

def Email_Exists(email):
    email = db.session.query(UserModel).filter(UserModel.email == email).scalar() is not None
    if email:
        return 'Mail already used', 409

def Admin_Status(claim):
    if claim['admin']:
        return True
    else:
        return False

def Seism_Exists(dtime):
    SeismE = db.session.query(SeismModel).filter(SeismModel.datime == dtime).scalar() is not None
    if SeismE:
        return True
    else:
        return False