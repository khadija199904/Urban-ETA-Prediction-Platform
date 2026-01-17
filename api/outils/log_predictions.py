from api.models.eta_predictions import ETAPrediction




def log_prediction(db,features, predicted_duration, model_version="v1.0"):
    
    
    eta_pred = ETAPrediction(
        trip_distance = features.trip_distance,
        fare_amount = features.fare_amount,
        tip_amount = features.tip_amount,
        total_amount = features.total_amount,
        cbd_congestion_fee = features.cbd_congestion_fee,
        pickup_hour = features.pickup_hour,
        day_of_week = features.day_of_week,
        month = features.month,
        ratecodeid = features.RatecodeID,
        payment_type = features.payment_type,
        estimated_duration = float(predicted_duration),
        model_version = model_version
    )
    
    db.add(eta_pred)
    db.commit()
    db.refresh(eta_pred)
    
    return eta_pred
