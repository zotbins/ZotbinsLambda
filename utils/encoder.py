from models.db_models import BinInfo, FullnessMetric, UsageMetric, WeightMetric
from datetime import datetime

def encode_bin_info_list(bins) -> None:
    "Encodes list of bin infos"
    for i in range(len(bins)):
        bins[i]  = encode_bin_info(bins[i])

def encode_bin_info(bin: BinInfo) -> dict:
    "Returns dictionary with BinInfo attributes"

    return {
        "id": bin.id,
        "uuid": bin.uuid,
        "latitude": bin.lat,
        "longitude": bin.lon,
        "bin_type": bin.bin_type.name
    }

def encode_fullness_info_list(fullnesses) -> None:
    "Encodes list of fullness metrics info"
    for i in range(len(fullnesses)):
        fullnesses[i]  = encode_fullness_info(fullnesses[i])

def encode_fullness_info(fullness: FullnessMetric) -> dict:
    "Returns dictionary with FullnessMetric attributes"

    return {
        "id": fullness.id,
        "timestamp": fullness.timestamp.isoformat(sep=' ', timespec='seconds'),
        "fullness": fullness.fullness,
        "sensor_id": fullness.sensor_id
    }

def encode_usage_info_list(usages) -> None:
    "Encodes list of usage metrics info"
    for i in range(len(usages)):
        usages[i]  = encode_usage_info(usages[i])

def encode_usage_info(usage: UsageMetric) -> dict:
    "Returns dictionary with UsageMetric attributes"

    return {
        "id": usage.id,
        "timestamp": usage.timestamp.isoformat(sep=' ', timespec='seconds'),
        "used_rate": usage.used_rate,
        "sensor_id": usage.sensor_id
    }

def encode_weight_info_list(weights) -> None:
    "Encodes list of usage metrics info"
    for i in range(len(weights)):
        weights[i]  = encode_weight_info(weights[i])

def encode_weight_info(weight: WeightMetric) -> dict:
    "Returns dictionary with WeightMetric attributes"

    return {
        "id": weight.id,
        "timestamp": weight.timestamp.isoformat(sep=' ', timespec='seconds'),
        "weight": weight.weight,
        "sensor_id": weight.sensor_id
    }