import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.pipeline import Pipeline
import joblib 
from database import engine
from math import sqrt



query = "SELECT * FROM silver_taxi"
print("Chargement des données depuis PostgreSQL...")

df = pd.read_sql(query, engine)

# Préparation des données (Preprocessing)
target = "trip_duree"
features = ["trip_distance","fare_amount","tip_amount","total_amount","cbd_congestion_fee","pickup_hour","day_of_week","month","RatecodeID","payment_type"]

X = df[features]
y = df[target]



# 4. Split Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# X_train_small = X_train.sample(10000, random_state=42)  # échantillon 10k lignes
# y_train_small = y_train.loc[X_train_small.index]



models = [
    ("LR", LinearRegression()),
    ("RF", RandomForestRegressor(n_estimators=20, max_depth=10, n_jobs=-1,random_state=42)),
    ("GBT", GradientBoostingRegressor(random_state=42))
]

# Boucle d'entraînement avec Pipeline
best_rmse = float('inf')
best_pipe = None
best_model_name = None

for name, model in models:
    print(f"\n--- Entraînement de : {name} ---")
    
    
   
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', model)
    ])

    # Entraînement
    pipeline.fit(X_train, y_train)
    # pipeline.fit(X_train_small, y_train_small)

    # Prédictions et évaluation
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred)
    rmse = sqrt(rmse)
    
    print(f"R²: {r2:.2f} | RMSE: {rmse:.2f}")
    if rmse < best_rmse:
        best_rmse = rmse
        best_pipe = pipeline
        best_model_name = name

# Sauvgarde le modele
filename = f"ML/models_pkl/{best_model_name}_Sklearn.pkl"
joblib.dump(best_pipe, filename)
print(f"\nMeilleur modèle sauvegardé dans  {filename} avec RMSE: {best_rmse:.2f}")





