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
    # Query the session and print out the results

    print()
    for entity in (BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor, WeightMetric, FullnessMetric, UsageMetric):
        print(f"Table:  {str(entity)[18:-2]}")
        for obj in session.query(entity).all():
            for value in list(obj.__dict__.values())[1:]:
                print(f"{value}", end = "    ")
            print()
        print()


