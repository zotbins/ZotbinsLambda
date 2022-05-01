from controllers.session_controller import session
from models.db_models import FullnessMetric, UsageMetric, WeightMetric
from datetime import datetime
from utils import encoder

def get_fullness_by_uuid(uuid: str) -> FullnessMetric:
    query_result = session.query(FullnessMetric).filter_by(uuid=uuid).first()
    
    if query_result:

        return {
            "fullness": query_result.fullness,
            "timestamp": query_result.timestamp
        }

    else:
        raise Exception

def get_usage_by_uuid(uuid: str) -> UsageMetric:
    query_result = session.query(UsageMetric).filter_by(uuid=uuid).first()
    
    if query_result:
        
        return {
            "usage": query_result.used_rate,
            "timestamp": query_result.timestamp
        }

    else:
        raise Exception

def get_weight_by_uuid(uuid: str) -> WeightMetric:
    query_result = session.query(WeightMetric).filter_by(uuid=uuid).first()
    
    if query_result:
        
        return {
            "weight": query_result.weight,
            "timestamp": query_result.timestamp
        }
        
    else:
        raise Exception

def get_all_fullness() -> None:
    query_result = session.query(FullnessMetric).all()
    encoder.encode_fullness_info_list(query_result)

    return query_result

def get_all_usage() -> None:
    query_result = session.query(UsageMetric).all()
    encoder.encode_usage_info_list(query_result)

    return query_result

def get_all_weight() -> None:
    query_result = session.query(WeightMetric).all()
    encoder.encode_weight_info_list(query_result)

    return query_result

def get_fullness_by_sensor_id_and_timestamp(sensor_id: str, start_time: datetime, end_time: datetime) -> FullnessMetric:
    query_result = session.query(FullnessMetric).filter_by(sensor_id=sensor_id).first()
    query_result_dict = encoder.encode_fullness_info(query_result)
    timestamp = datetime.strptime(query_result_dict["timestamp"][2:], "%y-%m-%d %H:%M:%S")
    if timestamp <= end_time and timestamp >= start_time:
        return query_result_dict
    else:
        raise Exception

def get_usage_by_sensor_id_and_timestamp(sensor_id: str, start_time: datetime, end_time: datetime) -> UsageMetric:
    query_result = session.query(UsageMetric).filter_by(sensor_id=sensor_id).first()
    query_result_dict = encoder.encode_usage_info(query_result)
    timestamp = datetime.strptime(query_result_dict["timestamp"][2:], "%y-%m-%d %H:%M:%S")
    if timestamp <= end_time and timestamp >= start_time:
        return query_result_dict
    else:
        raise Exception

def get_weight_by_sensor_id_and_timestamp(sensor_id: str, start_time: datetime, end_time: datetime) -> WeightMetric:
    query_result = session.query(WeightMetric).filter_by(sensor_id=sensor_id).first()
    query_result_dict = encoder.encode_weight_info(query_result)
    timestamp = datetime.strptime(query_result_dict["timestamp"][2:], "%y-%m-%d %H:%M:%S")
    if timestamp <= end_time and timestamp >= start_time:
        return query_result_dict
    else:
        raise Exception
    