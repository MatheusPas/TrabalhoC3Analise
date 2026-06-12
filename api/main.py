from fastapi import FastAPI
from database import engine, Base
import models
from routers import auth, houses, eda, features, regression, classification, clustering, pca

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hackathon House Prices API",
    description="API para análise de preços de casas nos EUA — FAESA 2024",
    version="2.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(houses.router, prefix="/api/v1/houses", tags=["Casas"])
app.include_router(eda.router, prefix="/api/v1/eda", tags=["EDA"])
app.include_router(features.router, prefix="/api/v1/features", tags=["Feature Engineering"])
app.include_router(regression.router, prefix="/api/v1/regression", tags=["Regressão"])
app.include_router(classification.router, prefix="/api/v1/classification", tags=["Classificação"])
app.include_router(clustering.router, prefix="/api/v1/clustering", tags=["Clusterização"])
app.include_router(pca.router, prefix="/api/v1/pca", tags=["PCA & Associação"])

@app.get("/")
def root():
    return {
        "message": "Hackathon House Prices API",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "online"
    }