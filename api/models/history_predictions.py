from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from api.database import Base  

class ETAPrediction(Base):
    __tablename__ = "eta_predictions"  
    

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Features du trajet
    trip_distance = Column(Float, nullable=False)
    fare_amount = Column(Float, nullable=True)
    tip_amount = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=True)
    cbd_congestion_fee = Column(Float, nullable=True)
    pickup_hour = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    ratecodeid = Column(Integer, nullable=True)
    payment_type = Column(Integer, nullable=True)
    
    # Prédiction et version du modèle
    estimated_duration = Column(Float, nullable=False)
    model_version = Column(String(20), nullable=False)
    
    # Timestamp automatique
    created_at = Column(DateTime(timezone=True), server_default=func.now())
