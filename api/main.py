from fastapi import FastAPI
from api.database import Base, engine
from api.routers import auth,predict
# from api.routers import predict,generate_plan



app = FastAPI(title="Urban ETA IA Plateforme ")


# Création des tables
Base.metadata.create_all(bind=engine)

#  Routes
app.include_router(auth.router)
app.include_router(predict.router)
# app.include_router(generate_plan.router)