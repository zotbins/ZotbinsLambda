
from db_models import BinType, BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor 
from db_models import WeightMetric, FullnessMetric, UsageMetric
from dummy_test_script import session

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


