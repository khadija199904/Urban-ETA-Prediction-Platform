from fastapi import APIRouter,Depends,HTTPException
from ..schemas.predict_schema import ETARequest , predictResponse
from ..services.prediction import get_prediction
from ..core.security import verify_token
from ..dependencies import get_db
from ..models.users import USERS
from ..outils.log_predictions import log_prediction


router = APIRouter(tags=['Predictions'])
MODEL_VERSION = "v1.0"

@router.post('/predict',response_model=predictResponse)
async def predict_ETA(features:ETARequest,token=Depends(verify_token),db = Depends(get_db)) :
    
    try:
        user = db.query(USERS).filter(USERS.username == token['Username']).first()
        if not user :
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
        eta_predictions = get_prediction(features)
    
        estimated_duree = round(eta_predictions[0],2)
        # Enregistrement dansla table  log_prediction
        eta_pred = log_prediction(db, features, estimated_duree, model_version=MODEL_VERSION)

    
    except ValueError as e:
        # Si les dimensions ou types sont incompatibles avec le modèle
        raise HTTPException(
            status_code=422,
            detail=f"Données incompatibles avec le modèle: {e}"
        )

    return  {"estimated_duration": estimated_duree}