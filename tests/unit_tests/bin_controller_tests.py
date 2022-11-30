
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

from setup_database import BinInfo, BinType, Sensor
from setup_database import session as test_session
import controllers.session_controller
controllers.session_controller.session = test_session

from controllers.bin_controller import *

def run_basic_bin_controller_query():
    # Tests that the controller correctly querries
    # the database by uuid
    test_bin = session.query(BinInfo).first()
    controller_bin = get_bin_by_uuid(test_bin.uuid)

    for attribute in ["uuid", "lat", "lon", "bin_type", "id"]:
        assert eval(f"test_bin.{attribute}") == eval(f"controller_bin.{attribute}"), f"Asserts that {attribute} is the same; test_bin: {test_bin.__dict__[attribute]}, controller_bin: {controller_bin.__dict__[attribute]}"



def run_basic_bin_controller_query_all():
    # Tests that the controller correctly queeries
    # all bins
    num_bins = len(session.query(BinInfo).all())
    num_bins_controller = len(get_all_bins())

    assert num_bins == num_bins_controller, "Asserts that the correct number of bins are returned by get_all_bins"


def run_basic_bin_controller_get_bin_location():
    # Tests that the controller correctly gets
    # the correct location of a bin
    test_bin = session.query(BinInfo).first()
    controller_bin = get_bin_location(test_bin.uuid)

    assert test_bin.__dict__["lat"] == controller_bin["latitude"], "Asserts that the bin location has the correct lattitude"
    assert test_bin.__dict__["lon"] == controller_bin["longitude"], "Asserts that the bin location has the correct lattitude"



def run_basic_bin_controller_update_bin_location():
    # Tests that the controller correctly updates
    # a bin's location
    test_bin = session.query(BinInfo).first()
    update_bin_location(test_bin.uuid, -1, -1)
    test_bin = session.query(BinInfo).filter_by(uuid=test_bin.uuid).first()
    controller_bin = get_bin_location(test_bin.uuid)
    assert test_bin.__dict__["lat"] == controller_bin["latitude"], "Asserts that the bin location has the correct lattitude"
    assert test_bin.__dict__["lon"] == controller_bin["longitude"], "Asserts that the bin location has the correct lattitude"



def run_basic_bin_controller_delete():
    # Tests that the controller correctly deletes a bin
    # from the database
    test_bin = session.query(BinInfo).first()
    bin_sensors = session.query(Sensor).filter_by(waste_bin_id=test_bin.id).all()

    previous_num_bins = len(session.query(BinInfo).all())

    delete_bin_by_uuid(test_bin.uuid)

    new_num_bins = len(session.query(BinInfo).all())
    assert previous_num_bins - 1 == new_num_bins, "Asserts that a bin was succesfully deleted"

    for sensor in bin_sensors:
         assert len(session.query(Sensor).filter_by(id=sensor.id).all()) == 0, "Asserts that after deleting a bin all sensors previously associated with the bin are deleted as well"


if __name__ == "__main__":
    run_basic_bin_controller_query()
    run_basic_bin_controller_query_all()
    run_basic_bin_controller_get_bin_location()
    run_basic_bin_controller_update_bin_location()
    run_basic_bin_controller_delete()
