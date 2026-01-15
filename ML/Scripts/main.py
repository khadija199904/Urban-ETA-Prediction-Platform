import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib 
from database import engine


query = "SELECT * FROM silver_taxi"
print("Chargement des données depuis PostgreSQL...")

df = pd.read_sql(query, engine)

# Préparation des données (Preprocessing)
target = "trip_duree"
features = ["trip_distance", "fare_amount", "tip_amount", "total_amount","cbd_congestion_fee", "pickup_hour", "day_of_week", "month"]

X = df[features]
y = df[target]



# 4. Split Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#  Entraînement du modèle (Gradient Boosting comme dans votre exemple Spark)
print("Entraînement du modèle Scikit-Learn...")
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train_scaled, y_train)

# 7. Évaluation
predictions = model.predict(X_test_scaled)
rmse = mean_squared_error(y_test, predictions, squared=False)
r2 = r2_score(y_test, predictions)

print(f"\nRésultats du modèle Scikit-Learn :")
print(f"R²: {r2:.4f}")
print(f"RMSE: {rmse:.4f}")

# # 8. Sauvegarde du modèle et du scaler
# import os
# os.makedirs("models_sklearn", exist_ok=True)

# joblib.dump(model, 'models_sklearn/gbt_model.pkl')
# joblib.dump(scaler, 'models_sklearn/scaler.pkl')

# print("Modèle sauvegardé dans 'models_sklearn/'")