
from db_models import BinType, BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor 
from db_models import WeightMetric, FullnessMetric, UsageMetric
from dummy_test_script import session

# Query the session and print out the results
q_list = []

bins = session.query(BinInfo).all()
q_list.append(bins)

sensors = session.query(Sensor).all()
q_list.append(sensors)

weight_sensors = session.query(WeightSensor).all()
q_list.append(weight_sensors)

fullness_sensors = session.query(FullnessSensor).all()
q_list.append(fullness_sensors)

usage_sensors = session.query(UsageSensor).all()
q_list.append(usage_sensors)

weight_metrics = session.query(WeightMetric).all()
q_list.append(weight_metrics)

fullness_metrics = session.query(FullnessMetric).all()
q_list.append(fullness_metrics)

usage_metrics = session.query(UsageMetric).all()
q_list.append(usage_metrics)

for i in q_list: print(i)