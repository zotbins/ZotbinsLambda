from controllers.session_controller import session
from models.db_models import FullnessMetric, UsageMetric, WeightMetric
from datetime import datetime

from utils import encoder


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
    query_result = session.query(FullnessMetric).filter(FullnessMetric.sensor_id == sensor_id, \
            FullnessMetric.timestamp >= start_time, \
            FullnessMetric.timestamp <= end_time).all()
    if query_result != []:
        encoder.encode_fullness_info_list(query_result)
        return query_result
    else:
        raise Exception


def get_usage_by_sensor_id_and_timestamp(sensor_id: str, start_time: datetime, end_time: datetime) -> UsageMetric:
    query_result = session.query(UsageMetric).filter(UsageMetric.sensor_id == sensor_id, \
            UsageMetric.timestamp >= start_time, \
            UsageMetric.timestamp <= end_time).all()
    if query_result != []:
        encoder.encode_usage_info_list(query_result)
        return query_result
    else:
        raise Exception


def get_weight_by_sensor_id_and_timestamp(sensor_id: str, start_time: datetime, end_time: datetime) -> WeightMetric:
    query_result = session.query(WeightMetric).filter(WeightMetric.sensor_id == sensor_id, \
            WeightMetric.timestamp >= start_time, \
            WeightMetric.timestamp <= end_time).all()
    if query_result != []:
        encoder.encode_weight_info_list(query_result)
        return query_result
    else:
        raise Exception


# # Unneeded functions as of right now
# # Unneeded as fullness metric does not have uuid attribute yet
# def get_fullness_by_uuid(uuid: str) -> FullnessMetric:
#     query_result = session.query(FullnessMetric).filter_by(uuid=uuid).first()
    
#     if query_result:

#         return {
#             "fullness": query_result.fullness,
#             "timestamp": query_result.timestamp
#         }

#     else:
#         raise Exception

# # Unneeded as usage metric does not have uuid attribute yet
# def get_usage_by_uuid(uuid: str) -> UsageMetric:
#     query_result = session.query(UsageMetric).filter_by(uuid=uuid).first()
    
#     if query_result:
        
#         return {
#             "usage": query_result.used_rate,
#             "timestamp": query_result.timestamp
#         }

#     else:
#         raise Exception

# # Unneeded as weight metric does not have uuid attribute yet
# def get_weight_by_uuid(uuid: str) -> WeightMetric:
#     query_result = session.query(WeightMetric).filter_by(uuid=uuid).first()
    
#     if query_result:
        
#         return {
#             "weight": query_result.weight,
#             "timestamp": query_result.timestamp
#         }
        
#     else:
#         raise Exception