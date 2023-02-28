import sys
import datetime
import os
import requests
 
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
    # Test Hard-Coded Data

    # ----- Check all weight metrics

    weight_metric_ids = [4,5,6]
    weight_metric_days = [15,14,13]
    for i in range(0,3):
        id = weight_metric_ids[i]
        day = weight_metric_days[i]
        req = requests.get(f"http://localhost:3000/weight_metrics/{id}/?start_timestamp=2023-02-{day} 00:00:00&end_timestamp=2023-02-{day} 00:00:01")
        if req.status_code == 200:
            j = req.json()[0]
            assert j["timestamp"] == f"2023-02-{day} 00:00:00"
            assert j["weight"] == 111
            assert j["sensor_id"] == id
        else:
            raise Exception(req.json()['detail'])

    # ----- Check all fullness metrics

    fullness_metric_ids = [7,8,9]
    fullness_metric_days = [15,14,13]
    for i in range(0,3):
        id = fullness_metric_ids[i]
        day = fullness_metric_days[i]
        req = requests.get(f"http://localhost:3000/fullness_metrics/{id}/?start_timestamp=2023-02-{day} 00:00:00&end_timestamp=2023-02-{day} 00:00:01")
        if req.status_code == 200:
            j = req.json()[0]
            assert j["timestamp"] == f"2023-02-{day} 00:00:00"
            assert j["fullness"] == 222
            assert j["sensor_id"] == id
        else:
            raise Exception(req.json()['detail'])
    
    # ----- Check all usage metrics

    usage_metric_ids = [10,11,12]
    usage_metric_days = [15,14,13]
    for i in range(0,3):
        id = usage_metric_ids[i]
        day = usage_metric_days[i]
        req = requests.get(f"http://localhost:3000/usage_metrics/{id}/?start_timestamp=2023-02-{day} 00:00:00&end_timestamp=2023-02-{day} 00:00:01")
        if req.status_code == 200:
            j = req.json()[0]
            assert j["timestamp"] == f"2023-02-{day} 00:00:00"
            assert j["used_rate"] == 3.0
            assert j["sensor_id"] == id
        else:
            raise Exception(req.json()['detail'])

    # ----- Check if bins present
    req = requests.get(f"http://localhost:3000/bins")
    if req.status_code == 200:
            bins = req.json()
            trash_present = False
            recycle_present = False
            compost_present = False
            for bin in bins:
                if bin['id'] == 1:
                    trash_present = True
                elif bin['id'] == 2:
                    recycle_present = True
                elif bin['id'] == 3:
                    compost_present = True
            assert trash_present
            assert recycle_present
            assert compost_present
    else:
        raise Exception(req.json()['detail'])