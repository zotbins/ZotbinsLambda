
import random

from db_models import base, db
from db_models import BinType, BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor 
from db_models import WeightMetric, FullnessMetric, UsageMetric
from sqlalchemy.orm import sessionmaker
#from sqlalchemy import DateTime
from datetime import datetime

# Generate database schema (place that stores all of the newly created entity objects)
base.metadata.create_all(db)

# Creates a new session
Session = sessionmaker(bind=db)

session = Session()

'''
# Functions
# Generates random BinInfo Objects
def gen_Bin():
    # Generates three random BinInfo Objects, one for every BinType
    for b_type in BinType:
        session.add(_gen_BinInfo(b_type))

def _gen_BinInfo(b_type: BinType):
    # Generates a specific BinInfo Object with the given bin type
    r_lat = random()
    BinInfo(id = , uuid = , lat = , lon = , bin_type = b_type)


# Generates random Sensor Object
def gen_Sensor():
    pass

# Generates random WeightSensor Object
def gen_WeightSensor():
    pass

# Generates random FullnessSensor Object
def gen_FullnessSensor():
    pass

# Generates random UsageSensor Object
def gen_UsageSensor():
    pass

# Generates random WeightMetric Object
def gen_WeightMetric():
    pass

# Generates random FullnessMetric Object
def gen_FullnessMetric():
    pass

# Generates random UsageMetric Object
def gen_UsageMetric():
    pass




'''


if __name__ == '__main__':

    '''
    # Puts all the possible ID's in a dictionary whose value is its associated object
    bins = session.query(BinInfo).all()

    sensors = session.query(Sensor).all()

    weight_metrics = session.query(WeightMetric).all()

    fullness_metrics = session.query(FullnessMetric).all()

    usage_metrics = session.query(UsageMetric).all()
    '''

    
    # Data to be inserted
    i_list = []

    # Manually insert dummy data into database
    # BinInfo
    wb_1_t = BinInfo(id = 6, uuid = "a", lat = 33.6405, lon = -117.8443, bin_type = BinType.T)
    i_list.append(wb_1_t)

    # Sensor
    wb_1_t_s = Sensor(id = 11, waste_bin_id = 6, measurement_units = 'kilograms', model = 'model A', make = '1')
    i_list.append(wb_1_t_s)

    # Component Sensors
    # WeightSensor
    wb_1_t_ws = WeightSensor(sensor_id = 11, configuration = 'kilograms', calibration_value = 1)
    i_list.append(wb_1_t_ws)

    # Metrics
    # WeightMetric
    wb_1_t_wm = WeightMetric(id = 12, timestamp = datetime.now(), weight = 20, sensor_id = 11)
    i_list.append(wb_1_t_wm)

    for i in i_list: session.add(i)
    

    # Commit and close session
    session.commit()

    session.close()