
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from unittest.mock import patch
from api.main import app  
from api.dependencies import get_db
from api.core.security import verify_token
from api.routers.analytics import moy_duree_par_heure 


client = TestClient(app)

def mock_verify_token():
    return {"Username":"fake_user"}
def mock_get_db():
    db = MagicMock()
    try:
        yield db
    finally:
        pass

@pytest.fixture(autouse=True)
def setup_dependencies():
    
    app.dependency_overrides[verify_token] = mock_verify_token
    app.dependency_overrides[get_db] = mock_get_db
    
    yield # Le test s'exécute ici
    
    app.dependency_overrides = {}

   
def test_payment_analysis():

    response = client.get("/analytics/payment-analysis")
    
    assert response.status_code == 200

    

# Mock pour GET /analytics/avg-duration-by-hour
def test_avg_duration_by_hour():
    mock_sql_rows = [
        ("08", 12.54),
        
    ]
   
    with patch("api.routers.analytics.execute_query") as mock_execute:
        mock_execute.return_value = mock_sql_rows

        response = client.get("/analytics/avg-duration-by-hour")
    assert response.status_code == 200
        
    mock_res = [
            {"pickuphour": "08", "avgduration": 12.5},
          
        ]
        
    assert response.json() == mock_res

# Mock pour POST /predict
def test_predict():
    mock_input = {
    "trip_distance": 5.2,
    "fare_amount": 15.0,
    "tip_amount": 2.5,
    "total_amount": 20.0,
    "cbd_congestion_fee": 2.5,
    "pickup_hour": 14,
    "day_of_week": 2,  # Mercredi
    "month": 6,
    "RatecodeID": 1,
    "payment_type": 1
    }



    with patch("api.routers.predict.get_prediction") as mock_get_pred, \
         patch("api.routers.predict.log_prediction") as mock_log:
        
    
        mock_get_pred.return_value = [15.5678]
        mock_log.return_value = True


        response = client.post("/predict", json=mock_input)
        assert response.status_code == 200
        assert response.json() == {"estimated_duration": 15.57}
