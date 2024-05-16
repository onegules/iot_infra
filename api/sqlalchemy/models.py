from sqlalchemy import Column, String, Integer, Float

from .databases import Base

class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True)
    serial = Column(Integer)
    event_time = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    air_pressure = Column(Float)
