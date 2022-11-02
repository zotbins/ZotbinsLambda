from models.db_models import BinInfo, FullnessMetric, UsageMetric, WeightMetric
from datetime import datetime

def encode_bin_info_list(bins: "list[BinInfo]") -> None:
    """
    Encodes each bin into a dictionary containing its attributes
    Parameters
    ----------
    bins: list[BinInfo]
        List of bins to encode
    Returns
    -------
    None
    """

    "Encodes list of bin infos"
    for i in range(len(bins)):
        bins[i] = encode_bin_info(bins[i])


def encode_bin_info(bin: BinInfo) -> dict:
    """
    Encodes a bin into a dictionary containing its attributes
    Parameters
    ----------
    bin: BinInfo
        Bin to encode
    Returns
    -------
    Returns a dict
        Contains the bin's attributes represented as a dictionary
    """

    "Returns dictionary with BinInfo attributes"
    return {
        "id": bin.id,
        "uuid": bin.uuid,
        "latitude": bin.lat,
        "longitude": bin.lon,
        "bin_type": bin.bin_type.name
    }

def encode_fullness_info_list(fullnesses: "list[FullnessMetric]") -> None:
    """
    Encodes each fullness metric into a dictionary containing its attributes
    Parameters
    ----------
    fullnesses: list[FullnessMetric]
        List of fullness metrics to encode
    Returns
    -------
    None
    """

    "Encodes list of fullness metrics info"
    for i in range(len(fullnesses)):
        fullnesses[i]  = encode_fullness_info(fullnesses[i])

def encode_fullness_info(fullness: FullnessMetric) -> dict:
    """
    Encodes a fullness metric into a dictionary containing its attributes
    Parameters
    ----------
    fullness: FullnessMetric
        Fullness metric to encode
    Returns
    -------
    Returns a dict
        Contains the fullness metric's attributes represented as a dictionary
    """

    "Returns dictionary with FullnessMetric attributes"

    return {
        "id": fullness.id,
        "timestamp": fullness.timestamp.isoformat(sep=' ', timespec='seconds'),
        "fullness": fullness.fullness,
        "sensor_id": fullness.sensor_id
    }

def encode_usage_info_list(usages: "list[UsageMetric]") -> None:
    """
    Encodes each usage metric into a dictionary containing its attributes
    Parameters
    ----------
    usages: list[UsageMetric]
        List of usage metrics to encode
    Returns
    -------
    None
    """
    
    "Encodes list of usage metrics info"
    for i in range(len(usages)):
        usages[i]  = encode_usage_info(usages[i])

def encode_usage_info(usage: UsageMetric) -> dict:
    """
    Encodes a usage metric into a dictionary containing its attributes
    Parameters
    ----------
    usage: UsageMetric
        Usage metric to encode
    Returns
    -------
    Returns a dict
        Contains the usage metric's attributes represented as a dictionary
    """

    "Returns dictionary with UsageMetric attributes"

    return {
        "id": usage.id,
        "timestamp": usage.timestamp.isoformat(sep=' ', timespec='seconds'),
        "used_rate": usage.used_rate,
        "sensor_id": usage.sensor_id
    }

def encode_weight_info_list(weights: "list[WeightMetric]") -> None:
    """
    Encodes each weight metric into a dictionary containing its attributes
    Parameters
    ----------
    weight: list[WeightMetric]
        List of weight metrics to encode
    Returns
    -------
    None
    """

    "Encodes list of usage metrics info"
    for i in range(len(weights)):
        weights[i]  = encode_weight_info(weights[i])

def encode_weight_info(weight: WeightMetric) -> dict:
    """
    Encodes a weight metric into a dictionary containing its attributes
    Parameters
    ----------
    weight: WeightMetric
        Weight metric to encode
    Returns
    -------
    Returns a dict
        Contains the weight metric's attributes represented as a dictionary
    """

    "Returns dictionary with WeightMetric attributes"

    return {
        "id": weight.id,
        "timestamp": weight.timestamp.isoformat(sep=' ', timespec='seconds'),
        "weight": weight.weight,
        "sensor_id": weight.sensor_id
    }