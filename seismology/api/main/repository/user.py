from ..resources import control_page
from ..repository import DataBaseRepository
from ..mapping import UserSchema
from ..models import UserModel
from ..extensions import db

UserSchema = UserSchema()
UserSSchema = UserSchema(many=True)

class User(DataBaseRepository):
    id = 0
    databaseSession = None
    instance = None
    jsonAdd = ""
    jsonImport = ""

    def s_id(self, id):
        self.id=id
    def s_databaseSession(self,session):
        self.databaseSession = session
    def s_instance(self, instance):
        self.instance=instance
    def s_jsonAdd(self, json):
        self.jsonAdd = json
    def s_jsonImport(self,json):
        self.jsonImport = json

    def allget(self):
        page = 1
        perpage = 100
        userlist = self.get_query()
        pagine = control_page(page, perpage, userlist)

        for key, value in self.jsonImport:
            users = page.apply(key, value)
        users, pagination = pagine.pagination()
        return UserSSchema.dump(users.all())

    def get(self):
        user = db.session.query(UserModel).get(self.id)
        return user

    def getIdUsersList(self):
        if self.databaseSession is not None:
            users = db.session.query(UserModel).all()
            ListIDs = []

            for user in users:
                ListIDs.append(user.id_num)
            return ListIDs

    def ok_OR404(self):
        user = db.session.query(UserModel).get_or_404(self.id)
        return user

    def add(self):
        if self.jsonAdd != "":
            instance = UserModel(email=self.jsonAdd.get("email"), plain_password=self.jsonAdd.get("password"), admin=self.jsonAdd.get("admin"))
            self.instance = instance

        if self.instance is not None:
            db.session.add(self.instance)

        return UserSchema.dump(self.instance), 201

    def edit(self):
        if self.instance is not None:
            for key, values in self.jsonImport:
                setattr(self.instance, key, values)
            return self.add()

    def delete(self):
        if self.instance is not None:
            db.session.delete(self.instance)
            db.session.commit()
        return 'User deleted', 204
