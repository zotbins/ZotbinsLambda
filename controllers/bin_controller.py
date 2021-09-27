from controllers.session_controller import session
from models.db_models import BinInfo

from utils import encoder


def get_bin_by_uuid(uuid: str) -> BinInfo:
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()
    return query_result


def delete_bin_by_uuid(uuid: str) -> None:
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()

    if query_result:
        session.delete(query_result)
        session.commit()
    else:
        raise Exception


def get_all_bins() -> None:
    query_result = session.query(BinInfo).all()
    encoder.encode_bin_info_list(query_result)

    return query_result


def get_bin_location(uuid: str) -> dict:
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()

    if query_result:
        return {
            "latitude": query_result.lat,
            "longitude": query_result.lon
        }
    else:
        raise Exception

def update_bin_location(uuid: str, new_lat: float, new_lon: float) -> None:
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()

    if query_result:
        query_result.lat = new_lat
        query_result.lon = new_lon

        session.add(query_result)
        session.commit()
    else:
        raise Exception
