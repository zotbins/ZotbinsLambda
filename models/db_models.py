import enum

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum

db = create_engine("postgresql://postgres:password@localhost:5432/postgres")
base = declarative_base()


class BinType(enum.Enum):
    T = "TRASH"
    R = "RECYCLABLE"
    C = "COMPOST"


class BinInfo(base):
    __tablename__ = "bin_info"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(8))
    lat = Column(Float)
    lon = Column(Float)
    bin_type = Column(Enum(BinType))


class Sensor(base):
    __tablename__ = "sensor"
    id = Column(Integer, primary_key=True)
    waste_bin_id = Column(Integer, ForeignKey("bin_info.id"))
    measurement_units = Column(String(64))
    model = Column(String(64))
    make = Column(String(64))


class WeightSensor(base):
    __tablename__ = "weight_sensor"
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    configuration = Column(String(64))
    calibration_value = Integer


class WeightMetric(base):
    __tablename__ = "weight_metric"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    weight = Column(Integer)
    sensor_id = Column(Integer, ForeignKey("weight_sensor.sensor_id"))


class FullnessSensor(base):
    __tablename__ = "fullness_sensor"
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    installed_where = Column(String)
    bin_height = Column(Integer)


class FullnessMetric(base):
    __tablename__ = "fullness_metric"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    fullness = Column(Integer)
    sensor_id = Column(Integer, ForeignKey("fullness_sensor.sensor_id"))


class UsageSensor(base):
    __tablename__ = "usage_sensor"
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    maximum_range = Column(Float)


class UsageMetric(base):
    __tablename__ = "usage_metric"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    used_rate = Column(Float)
    sensor_id = Column(Integer, ForeignKey("usage_sensor.sensor_id"))
