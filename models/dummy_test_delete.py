from db_models import BinType, BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor 
from db_models import WeightMetric, FullnessMetric, UsageMetric
from dummy_test_script import session

# Deletes ALL of the inserted Data

# Deletes ALL Metrics
weight_metrics = session.query(WeightMetric).delete()

fullness_metrics = session.query(FullnessMetric).delete()

usage_metrics = session.query(UsageMetric).delete()


# Deletes ALL Sensors
weight_sensors = session.query(WeightSensor).delete()

fullness_sensors = session.query(FullnessSensor).delete()

usage_sensors = session.query(UsageSensor).delete()

sensors = session.query(Sensor).delete()


# Deletes ALL Bins
bins = session.query(BinInfo).delete()

# Commit and close session
session.commit()

session.close()




