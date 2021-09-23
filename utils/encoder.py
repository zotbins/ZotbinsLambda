from models.db_models import BinInfo


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
