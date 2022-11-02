import enum

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

db = create_engine("postgresql://postgres:password@localhost:5432/postgres")
base = declarative_base()


class BinType(enum.Enum):
    T = "TRASH"
    R = "RECYCLABLE"
    C = "COMPOST"


class BinInfo(base):
    __tablename__ = "bin_info"
    uuid = Column(String(36))
    lat = Column(Float)
    lon = Column(Float)
    bin_type = Column(Enum(BinType))

    # ID
    id = Column(Integer, primary_key=True)

    # One to Many relationship with Sensor
    sensors = relationship("Sensor", cascade="all, delete-orphan")



class Sensor(base):
    __tablename__ = "sensor"
    measurement_units = Column(String(64))
    model = Column(String(64))
    make = Column(String(64))

    # ID
    id = Column(Integer, primary_key=True)

    # Many to One relationship with BinInfo
    waste_bin_id = Column(Integer, ForeignKey("bin_info.id"))

    # One to One relationship with sensors
    weight_sensor = relationship("WeightSensor", back_populates ='sensor', uselist = False, cascade="all, delete-orphan")
    fullness_sensor = relationship("FullnessSensor", back_populates ='sensor', uselist = False, cascade="all, delete-orphan")
    usage_sensor = relationship("UsageSensor", back_populates ='sensor', uselist = False, cascade="all, delete-orphan")



class WeightSensor(base):
    __tablename__ = "weight_sensor"
    configuration = Column(String(64))
    calibration_value = Integer

    # One to One relationship with sensor
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    sensor = relationship("Sensor", back_populates="weight_sensor")

    # One to Many relationship with WeightMetric
    weight_metric = relationship("WeightMetric", cascade="all, delete-orphan")



class WeightMetric(base):
    __tablename__ = "weight_metric"
    timestamp = Column(DateTime, primary_key=True)
    weight = Column(Integer)

    # One to Many relationship with WeightSensor
    sensor_id = Column(Integer, ForeignKey("weight_sensor.sensor_id"))



class FullnessSensor(base):
    __tablename__ = "fullness_sensor"
    installed_where = Column(String)
    bin_height = Column(Integer)

    # One to One relationship with sensor
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    sensor = relationship("Sensor", back_populates="fullness_sensor")

    # One to Many relationship with FullnessMetric
    fullness_metric = relationship("FullnessMetric", cascade="all, delete-orphan")



class FullnessMetric(base):
    __tablename__ = "fullness_metric"
    timestamp = Column(DateTime, primary_key=True)
    fullness = Column(Integer)

    # One to Many relationship with FullnessSensor
    sensor_id = Column(Integer, ForeignKey("fullness_sensor.sensor_id"))


class UsageSensor(base):
    __tablename__ = "usage_sensor"
    maximum_range = Column(Float)

    # One to One relationship with sensor
    sensor_id = Column(Integer, ForeignKey("sensor.id"), primary_key=True)
    sensor = relationship("Sensor", back_populates="usage_sensor")

    # One to Many relationship with WeightMetric
    usage_metric = relationship("UsageMetric", cascade="all, delete-orphan")


class UsageMetric(base):
    __tablename__ = "usage_metric"
    timestamp = Column(DateTime, primary_key=True)
    used_rate = Column(Float)

    # One to Many relationship with UsageSensor
    sensor_id = Column(Integer, ForeignKey("usage_sensor.sensor_id"))
