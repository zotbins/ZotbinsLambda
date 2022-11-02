
# TESTS BIN ENDPOINTS
import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from setup_database import BinInfo, BinType
from setup_database import session
from controllers.bin_controller import get_bin_by_uuid

def run_basic_bin_controller_query():
    # Tests that the controller correctly querries
    # the database by uuid
    test_bin = session.query(BinInfo).first()
    controller_bin = get_bin_by_uuid(test_bin.uuid)

    for attribute in ["uuid", "lat", "lon", "bin_type", "id"]:
        assert eval(f"test_bin.{attribute}") == eval(f"controller_bin.{attribute}"), f"Asserts that {attribute} is the same; test_bin: {test_bin.__dict__[attribute]}, controller_bin: {controller_bin.__dict__[attribute]}"

if __name__ == "__main__":
    run_basic_bin_controller_query()