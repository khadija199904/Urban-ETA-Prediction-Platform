from pydantic import BaseModel,Field

class ETARequest(BaseModel):

    trip_distance: float = Field(..., gt=0, description="Distance du trajet en miles")
    fare_amount: float = Field(..., ge=0, description="Tarif de base du trajet")
    tip_amount: float = Field(..., ge=0, description="Pourboire payé")
    total_amount: float = Field(..., ge=0, description="Somme totale payée")
    cbd_congestion_fee: float = Field(..., ge=0, description="Taxe zone CBD")
    pickup_hour: int = Field(..., ge=0, le=23, description="Heure de départ (0-23)")
    day_of_week: int = Field(..., ge=0, le=6, description="Jour de la semaine (0=Lundi, 6=Dimanche)")
    month: int = Field(..., ge=1, le=12, description="Mois du trajet (1-12)")
    RatecodeID: int = Field(..., ge=1, le=6, description="Code du type de tarif (1-6)")
    payment_type: int = Field(..., ge=0, le=5, description="Type de paiement (0=CASH, 1=CARD, etc.)")


class predictResponse(BaseModel):
    estimated_duration: float
