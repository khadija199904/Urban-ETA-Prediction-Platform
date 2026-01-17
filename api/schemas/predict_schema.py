from pydantic import BaseModel

class predictRequest(BaseModel):
    trip_distance: float
    passenger_count: int
    pickuphour: int
    day_of_week: int
    month: int
    payment_type: int



class prdictResponse(BaseModel):
    estimated_duration: float
