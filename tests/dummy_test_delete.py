# FOR MANUAL TESTING PURPOSES

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

from models.db_models import BinType, BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor 
from models.db_models import WeightMetric, FullnessMetric, UsageMetric
from setup_database import session


if __name__ == "__main__":
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


