from db_models import BinType, BinInfo, Sensor, WeightSensor, FullnessSensor, UsageSensor
from db_models import WeightMetric, FullnessMetric, UsageMetric
from dummy_test_script import session


def adding_new_bin_tests():
    previous_number_of_bins = len(session.query(BinInfo).all())
    new_bin = BinInfo(id=-1, uuid=-1, lat=-1, lon=-1, bin_type="T")

    session.add(new_bin)

    new_number_of_bins = len(session.query(BinInfo).all())
    assert previous_number_of_bins == new_number_of_bins - 1

    query_newly_added_bin = (session.query(BinInfo).filter(BinInfo.id == -1))
    query_not_existing_bin = (session.query(BinInfo).filter(BinInfo.id == -2))

    assert len(query_newly_added_bin.all()) == 1
    assert len(query_not_existing_bin.all()) == 0

def removing_bin_tests():
    query_bin_to_remove = (session.query(BinInfo).filter(BinInfo.id == -1))
    previous_number_of_bins = len(session.query(BinInfo).all())

    session.delete(query_bin_to_remove.all()[0])

    new_number_of_bins = len(session.query(BinInfo).all())

    assert new_number_of_bins == previous_number_of_bins - 1

    query_removed_bin = (session.query(BinInfo).filter(BinInfo.id == -1))
    assert len(query_removed_bin.all()) == 0



if __name__ == '__main__':
    adding_new_bin_tests()
    removing_bin_tests()
