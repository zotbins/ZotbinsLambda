from sqlalchemy import MetaData
from models import base, db
from models import BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor 
from models import WeightMetric, FullnessMetric, UsageMetric

tables_classes = [
    BinInfo.__table__,
    Sensor.__table__,
    WeightSensor.__table__,
    FullnessSensor.__table__,
    UsageSensor.__table__,
    WeightMetric.__table__,
    FullnessMetric.__table__,
    UsageMetric.__table__
]

base.metadata.create_all(db, tables=tables_classes)