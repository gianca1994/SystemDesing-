import secrets, random, string
from ..extensions import db
from ..repositories import DataBaseRepository
from ..repository.user import User as UserR
from ..resources import PageC
from ..mapping import SensorSchema
from ..models import SensorModel

SensorSchema = SensorSchema()
SensorsSchema = SensorSchema(many=True)

class Sensor(DataBaseRepository):
    id = 0
    databaseSession = None
    instance = None
    jsonAdd = ""
    jsonImport = ""

    def s_id(self, id):
        self.id = id
    def s_instance(self, instance):
        self.instance = instance
    def s_jsonImport(self, json):
        self.jsonImport = json
    def s_jsonAdd(self, json):
        self.jsonAdd = json
    def s_databaseSession(self, session):
        self.databaseSession = session

    def allget(self):
        page = 1
        perpage = 10
        sensors = self.get_query()
        pag = PageC(sensors, page, perpage)

        for key, val in self.jsonImport:
            sensors = pag.apply(key, val)
        sensors, _pagination = pag.pagination()
        return SensorsSchema.dump(sensors.all())

    def getIdSensorList(self):
        if self.databaseSession is not None:
            id_list = []
            sensors = self.databaseSession.query(SensorModel).all()
            for sensor in sensors:
                id_list.append(sensor.id_num)
            return id_list

    def ok_OR404(self):
        sensor = db.session.query(SensorModel).get_or_404(self.id)
        return sensor

    def get(self):
        sensor = db.session.query(SensorModel).get(self.id)
        return sensor

    def getQuery(self):
        sensor = db.session.query(SensorModel)
        return sensor

    def add(self):
        if self.jsonAdd != "":
            self.instance = SensorSchema.load(self.jsonAdd, session=db.session)
        else:
            UserR = UserR()
            UserR.s_databaseSession(db.session)
            sensor = SensorModel(name=''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(3)),
                ip=".".join(map(str, (random.randint(0, 255) for _ in range(4)))),
                port=''.join(map(str, (random.randint(0, 9) for _ in range(4)))),
                status=bool(random.getrandbits(1)), active=bool(random.getrandbits(1)),
                userId=int(random.choice(UserR.getIdUsersList())))
            self.instance = sensor

        db.session.add(self.instance)
        db.session.commit()
        return SensorSchema.dump(self.instance), 201

    def edit(self):
        if self.instance is not None:
            for key, val in self.jsonImport:
                if key == 'userId':
                    Ruser = UserR()
                    Ruser.s_id(val)
                    Ruser.ok_OR404()
                    setattr(self.instance, key, val)
                else:
                    setattr(self.instance, key, val)
            return self.add()

    def delete(self):
        if self.instance is not None:
            db.session.delete(self.instance)
            db.session.commit()
            return 'Sensor cleared', 204

