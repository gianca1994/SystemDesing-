from datetime import datetime
from ..extensions import db
from ..models import SeismModel, SensorModel
from ..repository import DataBaseRepository
from ..resources import PageC, Seism_Exists
from ..maping import SeismSchema

SeismSchemaC = SeismSchema(session=db.session)
SeismsSchemaC = SeismSchema(many=True, session=db.session)


class Seism(DataBaseRepository):

    def __init__(self):
        self.userId = 0
        self.idSeism = 0
        self.jsonImport = ""
        self.jsonAdd = ""
        self.instance = None
        self.admin = None
        self.verif = None

    def s_userId(self, userId):
        self.userId = userId
    def s_idSeism(self, idSeism):
        self.idSeism = idSeism
    def s_jsonImport(self, json):
        self.jsonImport = json
    def s_jsonAdd(self, json):
        self.jsonAdd = json
    def s_instance(self, instance):
        self.instance = instance
    def s_adminVal(self, val):
        self.admin = val

    def allget(self):
        page = 1
        perpage = 15
        seisms = self.getQuery()
        pag = PageC(seisms, page, perpage)

        if self.userId != 0 and self.admin is not None:
            if not self.admin:
                seisms = self.getIdSeismsList()
            else:
                seisms = self.getQuery()

        for key, val in self.jsonImport:
            seisms = pag.apply(key, val)
            seisms, _pagination = pag.pagination()
        return SeismsSchemaC.dump(seisms.all())

    def getIdSeismsList(self):
        seisms = self.getQuery()
        seism = seisms.filter(SensorModel.userId == self.userId)
        return seism

    def ok_OR404(self):
        seism = db.session.query(SeismModel).get_or_404(self.idSeism)
        return seism

    def get(self):
        seism = db.session.query(SeismModel).get(self.idSeism)
        return seism

    def getQuery(self):
        seism = db.session.query(SeismModel).filter(SeismModel.verified == self.verif)
        return seism

    def add(self):
        if self.jsonAdd != "":
            instance = SeismSchemaC.loads(self.jsonAdd)
            SeismSchemaC.verified = self.verif
            SeismExis = Seism_Exists(dtime=datetime)
            if SeismExis:
                return 'The earthquake already exists', 409
            else:
                self.instance = instance

        if self.instance is not None:
            db.session.add(self.instance)
            db.session.commit()
            return SeismSchemaC.dump(self.instance), 201

    def edit(self):
        if self.instance is not None:
            for key, value in self.jsonImport:
                if key == 'datetime':
                    setattr(self.instance, key, datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
                else:
                    setattr(self.instance, key, value)
            return self.add()

    def delete(self):
        if self.instance is not None:
            db.session.delete(self.instance)
            db.session.commit()
            return 'The earthquake was erased', 204
