
# TESTS BIN ENDPOINTS

from base import *
from setup_database import BinInfo, BinType
from setup_database import session


def run_basic_bin_get_test():
    trash_bin = session.query(BinInfo).filter_by(bin_type=BinType.T).first()

    trash_bin_request = GET("http://localhost:3000", f"bin/{trash_bin.uuid}")

    assert(trash_bin.__dict__["id"] == trash_bin_request["id"])
    assert(trash_bin.__dict__["uuid"] == trash_bin_request["uuid"])
    assert(trash_bin.__dict__["lat"] == trash_bin_request["latitude"])
    assert(trash_bin.__dict__["lon"] == trash_bin_request["longitude"])
    


def run_basic_bin_post_test():
    pass

def run_basic_bin_delete_test():
    pass

if __name__ == "__main__":
    run_basic_bin_get_test()
    run_basic_bin_post_test()
    run_basic_bin_delete_test()