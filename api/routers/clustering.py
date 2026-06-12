from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import get_current_user
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
import numpy as np

router = APIRouter()

def get_dataframe(db: Session):
    houses = db.query(models.House).all()
    return pd.DataFrame([{
        "id": h.id, "lot_area": h.lot_area, "overall_qual": h.overall_qual,
        "overall_cond": h.overall_cond, "year_built": h.year_built,
        "gr_liv_area": h.gr_liv_area, "full_bath": h.full_bath,
        "half_bath": h.half_bath, "bedroom_abvgr": h.bedroom_abvgr,
        "totrms_abvgrd": h.totrms_abvgrd, "garage_cars": h.garage_cars,
        "garage_area": h.garage_area, "sale_price": h.sale_price
    } for h in houses]).dropna()

@router.get("/kmeans")
def kmeans(
    n_clusters: int = 3,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    features = [
        "lot_area", "overall_qual", "gr_liv_area",
        "garage_area", "sale_price"
    ]
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = model.fit_predict(X)
    summary = df.groupby("cluster")[features].mean().round(2)
    elbow = {}
    for k in range(2, 8):
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X)
        elbow[k] = round(km.inertia_, 2)
    return {
        "usuario": current_user,
        "n_clusters": n_clusters,
        "elbow": elbow,
        "perfil_clusters": summary.to_dict(orient="index"),
        "distribuicao": df["cluster"].value_counts().to_dict()
    }

@router.get("/outliers")
def outliers(
    n_neighbors: int = 20,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    features = [
        "lot_area", "overall_qual", "gr_liv_area",
        "garage_area", "sale_price"
    ]
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])
    lof = LocalOutlierFactor(n_neighbors=n_neighbors)
    df["lof_score"] = lof.fit_predict(X)
    df["lof_factor"] = lof.negative_outlier_factor_
    outliers_df = df[df["lof_score"] == -1][["id", "sale_price", "gr_liv_area", "overall_qual", "lof_factor"]]
    return {
        "usuario": current_user,
        "total_outliers": len(outliers_df),
        "outliers": outliers_df.sort_values("lof_factor").head(20).to_dict(orient="records")
    }