from sqlalchemy import Column, Integer, Float
from api.database import Base

class SilverTaxi(Base):
    __tablename__ = "silver_taxi"
    __table_args__ = {"schema": "silver", "extend_existing": True}

    # Pas de clé primaire explicite dans Spark
    # → SQLAlchemy en a besoin
    id = Column(Integer, primary_key=True, autoincrement=True)

    trip_distance = Column(Float)
    RatecodeID = Column(Integer)
    payment_type = Column(Integer)

    fare_amount = Column(Float)
    tip_amount = Column(Float)
    total_amount = Column(Float)

    cbd_congestion_fee = Column(Float)

    trip_duree = Column(Float)

    pickup_hour = Column(Integer)
    day_of_week = Column(Integer)
    month = Column(Integer)
