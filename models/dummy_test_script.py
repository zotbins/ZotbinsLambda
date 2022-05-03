
import random
from nanoid import generate
import sys

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


# Functions
# Generates a Bin (three bin types, three sensors for each bin type)
def gen_Bin(id_dict: dict, session: Session):
    ''' 
    Generates three random BinInfo Objects, one for every BinType and then calls gen_Sensors which
    will generate three random sensors for each BinInfo Object
    '''
    for b_type in BinType:

        ran_id = _gen_id(id_dict)
        r_lat = random.uniform(-90,90)
        r_lon = random.uniform(-180,180)

        new_bin = _gen_BinInfo(ran_id, b_type, r_lat, r_lon, session)

        session.add(new_bin)

        id_dict[ran_id] = type(new_bin)

        gen_Sensors(id_dict, session, ran_id)
    


def _gen_BinInfo(ran_id: int, b_type: BinType, r_lat: float, r_lon: float, session: Session):
    # Helper function that generates a specific BinInfo Object with the given bin type

    uuid_list = [b.uuid for b in session.query(BinInfo)]
    r_uuid = generate(size=8)
    while r_uuid in uuid_list: r_uuid = generate(size=8)

    return BinInfo(id = ran_id, uuid = r_uuid, lat = r_lat, lon = r_lon, bin_type = b_type)



# Generates all three sensors for a specific bin type
def gen_Sensors(id_dict: dict, session: Session, bin_id: int):
    # Generates a WeightSensor, FullnessSensor, and UsageSesnsor for the given BinInfo object
    for sensor_fun in [gen_WeightSensor,gen_FullnessSensor,gen_UsageSensor]:
        ran_id = _gen_id(id_dict)

        r_measurement_units = 'mm' if sensor_fun == gen_FullnessSensor else ("Number of Trash thrown away within 30 minute interval" if sensor_fun == gen_UsageSensor else "kg")
        r_model = 'Ultrasonic' if sensor_fun == gen_FullnessSensor else ("Breakbeam" if sensor_fun == gen_UsageSensor else "Lidar")
        r_make = 'version 1'

        session.add(Sensor(id = ran_id, measurement_units = r_measurement_units, model = r_model, make = r_make, waste_bin_id = bin_id))

        new_sensor = sensor_fun(ran_id, session)
        session.add(new_sensor)
        id_dict[ran_id] = type(new_sensor)




# Generates random WeightSensor Object
def gen_WeightSensor(ran_id: int, session: Session):
    # Generates a random WeightSensor Object given its sensor ID

    r_configuration = 'defualt'
    r_calibration_value = random.uniform(-0.0001, 0.0001)

    return WeightSensor(sensor_id = ran_id, configuration = r_configuration, calibration_value = r_calibration_value)



# Generates random FullnessSensor Object
def gen_FullnessSensor(ran_id: int, session: Session):
    # Generates a random FullnessSensor Object given its sensor ID

    r_installed_where = 'Top of Bin'
    r_bin_height = 48

    return FullnessSensor(sensor_id = ran_id, installed_where = r_installed_where, bin_height = r_bin_height)



# Generates random UsageSensor Object
def gen_UsageSensor(ran_id: int, session: Session):
    # Generates a random UsageSensor Object given its sensor ID

    r_maximum_range = random.randint(0,sys.maxsize)

    return UsageSensor(sensor_id = ran_id, maximum_range = r_maximum_range)



# Generates random WeightMetric Object
def gen_WeightMetric(id_dict: dict, session: Session, possible_sensors: list):
    # Generates a random WeightMetric Object for a random corresponding sensor only if there is a possible corresponding sensor

    if len(possible_sensors) > 0:
        sen_id = possible_sensors[random.randint(0,len(possible_sensors)-1)]

        ran_id = _gen_id(id_dict)
        r_weight = random.uniform(0,50)
        r_timestamp = datetime.now()
        
        new_weight_metric = WeightMetric(id = ran_id, weight = r_weight, timestamp = r_timestamp, sensor_id = sen_id)
        session.add(new_weight_metric)
        id_dict[ran_id] = type(new_weight_metric)



# Generates random FullnessMetric Object
def gen_FullnessMetric(id_dict: dict, session: Session, possible_sensors: list):
    # Generates a random WeightMetric Object for a random corresponding sensor only if there is a possible corresponding sensor

    if len(possible_sensors) > 0:
        sen_id = possible_sensors[random.randint(0,len(possible_sensors)-1)]

        ran_id = _gen_id(id_dict)
        r_fullness = random.randint(0,100)
        r_timestamp = datetime.now()
        
        new_fullness_metric = FullnessMetric(id = ran_id, fullness = r_fullness, timestamp = r_timestamp, sensor_id = sen_id)
        session.add(new_fullness_metric)
        id_dict[ran_id] = type(new_fullness_metric)



# Generates random UsageMetric Object
def gen_UsageMetric(id_dict: dict, session: Session, possible_sensors: list):
    # Generates a random WeightMetric Object for a random corresponding sensor only if there is a possible corresponding sensor

    if len(possible_sensors) > 0:
        sen_id = possible_sensors[random.randint(0,len(possible_sensors)-1)]

        ran_id = _gen_id(id_dict)
        r_used_rate = random.randint(0,20)
        r_timestamp = datetime.now()

        new_usage_metric = UsageMetric(id = ran_id, used_rate = r_used_rate, timestamp = r_timestamp, sensor_id = sen_id)
        session.add(new_usage_metric)
        id_dict[ran_id] = type(new_usage_metric)




#Helper Functions
# Helper function to get all the IDs in the database
def _get_ids(id_dict: dict, entity, session: Session):
    # Generates all the ID's of a certain entity and adds them to the passed in dict
    for obj in session.query(entity).all():
        if type(obj) in (WeightSensor, FullnessSensor, UsageSensor):
            assert obj.sensor_id not in id_dict, "Multiple Sensors with the same ID"
            id_dict[obj.sensor_id] = type(obj)
        else:
            id_dict[obj.id] = type(obj)


# Helper function that generates a random ID
def _gen_id(id_dict: dict):
    while True:
        ran_id = random.randint(0,9999)
        if ran_id not in id_dict:
            return ran_id





if __name__ == '__main__':
 
    # Puts all the possible ID's in a dictionary whose value is its associated object
    id_dict = dict()
    for entity in [BinInfo,WeightSensor,FullnessSensor,UsageSensor,WeightMetric,FullnessMetric,UsageMetric]: _get_ids(id_dict, entity, session)

    #Generates Random Bin
    if input('Would you like to create a new bin, which is 3 BinInfo objects and 9 sensor objects? (type yes for yes, anything else for no): ') == "yes":
        gen_Bin(id_dict, session)

    #Gathers possible Usage, Weight, and Fullness Sensors
    fullness_sensors = [identification for identification, obj_type in id_dict.items() if obj_type == FullnessSensor] 
    usage_sensors = [identification for identification, obj_type in id_dict.items() if obj_type == UsageSensor]
    weight_sensors = [identification for identification, obj_type in id_dict.items() if obj_type == WeightSensor]


    #Generates 5 pieces of random weight metric data
    for _ in range(5):
        gen_WeightMetric(id_dict, session, weight_sensors)
        gen_UsageMetric(id_dict, session, usage_sensors)
        gen_FullnessMetric(id_dict, session, fullness_sensors)

    # Commit and close session
    session.commit()

    session.close()