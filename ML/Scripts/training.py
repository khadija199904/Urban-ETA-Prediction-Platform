import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import joblib
from math import sqrt
import os
from api.database import engine

def train_model():

    print("Chargement des données depuis PostgreSQL...")

    query = "SELECT * FROM silver_taxi"
    df = pd.read_sql(query, engine)

    # Préparation des données
    target = "trip_duree"
    features = [
        "trip_distance", "fare_amount", "tip_amount", "total_amount",
        "cbd_congestion_fee", "pickup_hour", "day_of_week",
        "month", "RatecodeID", "payment_type"
    ]

    X = df[features]
    y = df[target]

    # Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    models = [
        ("LR", LinearRegression()),
        ("RF", RandomForestRegressor(
            n_estimators=20, max_depth=10, n_jobs=-1, random_state=42
        )),
        ("GBT", GradientBoostingRegressor(random_state=42))
    ]

    best_rmse = float("inf")
    best_pipe = None
    best_model_name = None

    for name, model in models:
        print(f"\n--- Entraînement de : {name} ---")

        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", model)
        ])

        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = sqrt(mean_squared_error(y_test, y_pred))

        print(f"R²: {r2:.2f} | RMSE: {rmse:.2f}")

        if rmse < best_rmse:
            best_rmse = rmse
            best_pipe = pipeline
            best_model_name = name

    # Sauvegarde du modèle
    os.makedirs("ML/models_pkl", exist_ok=True)
    filename = f"ML/models_pkl/{best_model_name}_Sklearn.pkl"

    joblib.dump(best_pipe, filename)

    print(
        f"\nMeilleur modèle sauvegardé : {filename} " f"avec RMSE = {best_rmse:.2f}"  )
