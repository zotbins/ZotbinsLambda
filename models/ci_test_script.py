from db_models import BinInfo, FullnessSensor, UsageSensor, WeightSensor
from dummy_test_script import _get_ids, session, gen_Bin, gen_FullnessMetric, gen_UsageMetric, gen_WeightMetric

if __name__ == '__main__':
    # Puts all the possible ID's in a dictionary whose value is its associated object
    id_dict = dict()
    # for entity in [BinInfo,WeightSensor,FullnessSensor,UsageSensor,WeightMetric,FullnessMetric,UsageMetric]: _get_ids(id_dict, entity, session)
    for entity in [BinInfo, WeightSensor, FullnessSensor, UsageSensor]: _get_ids(id_dict, entity, session)

    # Generates Random Bin
    gen_Bin(id_dict, session)

    # Gathers possible Usage, Weight, and Fullness Sensors
    fullness_sensors = [identification for identification, obj_type in id_dict.items() if obj_type == FullnessSensor]
    usage_sensors = [identification for identification, obj_type in id_dict.items() if obj_type == UsageSensor]
    weight_sensors = [identification for identification, obj_type in id_dict.items() if obj_type == WeightSensor]

    # Asks user how much metric data they would like to create
    num_data = 100

    # Generates data for ALL SENSORS given the user inputted ammount
    for f_sensor_id in fullness_sensors:
        gen_FullnessMetric(session, f_sensor_id, num_data)

    for u_sensor_id in usage_sensors:
        gen_UsageMetric(session, u_sensor_id, num_data)

    for w_sensor_id in weight_sensors:
        gen_WeightMetric(session, w_sensor_id, num_data)

    # Commit and close session
    session.commit()

    session.close()