import os
import pandas as pd
from api.outils.load_model import load_model
from fastapi import HTTPException
 
MODEL_PATH = os.path.join("ML", "models_pkl", "RF_Sklearn.pkl")

def get_prediction(features):

    # Charge le modèle 
    model = load_model(MODEL_PATH)
    if model is None:
        raise HTTPException(status_code=503, detail="Le service de prédiction est indisponible (Modèle non chargé).")

    try:
        eta_features = pd.DataFrame([features.model_dump()])
        predictions = model.predict(eta_features)
        return predictions
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Données incompatibles avec le modèle: {e}")