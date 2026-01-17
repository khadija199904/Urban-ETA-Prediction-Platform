from fastapi import APIRouter, Depends ,HTTPException
from ..core.security import verify_token
from ..dependencies import get_db
from ..models.users import USERS
from ..outils.execute_query import execute_query





router = APIRouter(tags=['Analytics'])


@router.get('/analytics/avg-duration-by-hour')
def moy_duree_par_heure(token=Depends(verify_token),db = Depends(get_db)):
     
    try:
        user = db.query(USERS).filter(USERS.username == token['Username']).first()
        if not user :
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")

        query = """
        
            WITH Analytics_Hourly AS (
                SELECT pickup_hour ,
                        AVG(trip_duree) AS avg_duree
                From silver_taxi
                GROUP BY pickup_hour
            )
            SELECT * FROM Analytics_Hourly
            WHERE avg_duree > 10
            ORDER BY pickup_hour ASC;
            """
    
        rows = execute_query(db,query)

        result = [
            {
                "pickuphour": r[0],
                "avgduration": round(r[1],1)
            }
            for r in rows
        ]

        return result
    
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))
 

@router.get('/analytics/payment-analysis') 
def analyse_payments(token=Depends(verify_token),db = Depends(get_db)) :
    try:
        user = db.query(USERS).filter(USERS.username == token['Username']).first()
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable")
        query = """
        
            WITH analytics_Payment AS (
                SELECT
                    payment_type,
                    COUNT(*) AS total_trips,
                    AVG(trip_duree) AS avg_duration
                From public.silver_taxi
                GROUP BY payment_type
            )
            SELECT * FROM analytics_Payment
            ORDER BY payment_type;
            """
        
        rows = execute_query(db,query)

        
        result = [
            {
                "payment_type": r[0],
                "total_trips": r[1],
                "avg_duration": round(r[2],1)  
            }
            for r in rows
        ]

        return result
    
    except Exception as e:
        # Gestion des erreurs
        raise HTTPException(status_code=500, detail=str(e))