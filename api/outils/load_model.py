import joblib
import os
from fastapi import HTTPException,status

def load_model(model_path):
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Modèle du Prediction introuvable : {model_path}"
        )
    try:
        # 2. Charger le modèle
        model = joblib.load(model_path)
        
        return model
    
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Erreur interne lors du chargement du modèle: {e}"
                   )




if __name__ == "__main__":

    MODEL_PATH = os.path.join("ML", "models_pkl", "RF_Sklearn.pkl")
    mo =load_model(MODEL_PATH)
    print(mo)
    
