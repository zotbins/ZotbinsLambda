from db_models import base, db
from db_models import BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor
from db_models import WeightMetric, FullnessMetric, UsageMetric

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

# automates creating tables
base.metadata.create_all(db, tables=tables_classes)

# TODO: Automate insertion of test data
# This is a hello world commit to the dummy_test branch