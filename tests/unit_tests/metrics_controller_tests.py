
# TESTS BIN ENDPOINTS
import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from setup_database import WeightMetric, FullnessMetric, UsageMetric
from setup_database import WeightSensor, FullnessSensor, UsageSensor
from controllers.metrics_controller import *
from datetime import datetime
from setup_database import session

def run_basic_metrics_controller_get_all_for_all_metric_types():
    # Tests the get all controllers for every metric type
   assert len(session.query(FullnessMetric).all()) == len(get_all_fullness()), "Asserts get_all_fullness returns all fullness metrics"
   assert len(session.query(UsageMetric).all()) == len(get_all_usage()), "Asserts get_all_usage returns all usage metrics"
   assert len(session.query(WeightMetric).all()) == len(get_all_weight()), "Asserts get_all_weight returns all weight metrics"


def run_basic_metrics_controller_get_all_metrics_by_sensor_id_and_timestamp_for_all_metric_types():
    # Tests the get by sensor id and timestamp controllers for every metric type
    # tests for all metrics ever inserted for these sensors
    fullness_sensor=session.query(FullnessSensor).first()
    usage_sensor=session.query(UsageSensor).first()
    weight_sensor=session.query(WeightSensor).first()
    assert len(session.query(FullnessMetric).filter_by(sensor_id=fullness_sensor.sensor_id).all())==len(get_fullness_by_sensor_id_and_timestamp(f"{fullness_sensor.sensor_id}", datetime(1,1,1), datetime.now()))
    assert len(session.query(UsageMetric).filter_by(sensor_id=usage_sensor.sensor_id).all())==len(get_usage_by_sensor_id_and_timestamp(f"{usage_sensor.sensor_id}", datetime(1,1,1), datetime.now()))
    assert len(session.query(WeightMetric).filter_by(sensor_id=weight_sensor.sensor_id).all())==len(get_weight_by_sensor_id_and_timestamp(f"{weight_sensor.sensor_id}", datetime(1,1,1), datetime.now()))


def run_basic_metrics_controller_get_recent_metrics_by_sensor_id_and_timestamp_for_all_metric_types():
    pass


if __name__ == "__main__":
    run_basic_metrics_controller_get_all_for_all_metric_types()
    run_basic_metrics_controller_get_all_metrics_by_sensor_id_and_timestamp_for_all_metric_types()
    run_basic_metrics_controller_get_recent_metrics_by_sensor_id_and_timestamp_for_all_metric_types()
