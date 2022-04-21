from models.db_models import BinInfo


def encode_bin_info_list(bins: [BinInfo]) -> None:
    """
    Encodes each bin into a dictionary containing its attributes
    Parameters
    ----------
    bins: [BinInfo]
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
