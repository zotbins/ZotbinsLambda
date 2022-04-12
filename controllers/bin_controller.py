from controllers.session_controller import session
from models.db_models import BinInfo

from utils import encoder


def get_bin_by_uuid(uuid: str) -> BinInfo:
    """
    Queries the database and retrieves bin associated with a unique uuid
    Parameters
    ----------
    uuid: str
        Unique id associated with a bin
    Returns
    -------
    Returns a BinInfo object: BinInfo
        BinInfo object associated with the uuid
    """
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()
    return query_result


def delete_bin_by_uuid(uuid: str) -> None:
    """
    Queries the database and deletes bin associated with a unique uuid
    Throws an Exception if bin associated with uuid doesn't exist
    Parameters
    ----------
    uuid: str
        Unique id associated with a bin
    Returns
    -------
    None
    """
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()

    if query_result:
        session.delete(query_result)
        session.commit()
    else:
        raise Exception


def get_all_bins() -> [dict]:
    """
    Returns
    -------
    Returns a list of dictionaries: [dict]
        Each dictionary contains a bin's attributes
    """
    query_result = session.query(BinInfo).all()
    encoder.encode_bin_info_list(query_result)

    return query_result


def get_bin_location(uuid: str) -> dict:
    """
    Queries the database and retrieves bin's location associated with a unique uuid
    Throws an Exception if bin associated with uuid doesn't exist
    Parameters
    ----------
    uuid: str
        Unique id associated with a bin
    Returns
    -------
    Returns a dict: dict
        Dictionary containing coordinates (latitude,longitude) for the bin associated with the uuid
    """
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()

    if query_result:
        return {
            "latitude": query_result.lat,
            "longitude": query_result.lon
        }
    else:
        raise Exception


def update_bin_location(uuid: str, new_lat: float, new_lon: float) -> None:
    """
    Queries the database and updates bin's location associated with a unique uuid
    Throws an Exception if bin associated with uuid doesn't exist
    Parameters
    ----------
    uuid: str
        Unique id associated with a bin
    new_lat: float
        Bin's new location latitude
    new_lon: float
        Bin's new location longitude
    Returns
    -------
    None
    """
    query_result = session.query(BinInfo).filter_by(uuid=uuid).first()

    if query_result:
        query_result.lat = new_lat
        query_result.lon = new_lon

        session.add(query_result)
        session.commit()
    else:
        raise Exception
