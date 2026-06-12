from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import get_current_user
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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

@router.get("/run")
def run_pca(
    n_components: int = 2,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    features = [
        "lot_area", "overall_qual", "overall_cond", "year_built",
        "gr_liv_area", "full_bath", "half_bath", "bedroom_abvgr",
        "totrms_abvgrd", "garage_cars", "garage_area"
    ]
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X)
    variance = pca.explained_variance_ratio_
    cumulative = np.cumsum(variance)
    loadings = pd.DataFrame(
        pca.components_.T,
        index=features,
        columns=[f"PC{i+1}" for i in range(n_components)]
    ).round(4)
    sample = pd.DataFrame(
        components[:10],
        columns=[f"PC{i+1}" for i in range(n_components)]
    ).round(4)
    return {
        "usuario": current_user,
        "n_components": n_components,
        "variancia_explicada": [round(v, 4) for v in variance.tolist()],
        "variancia_acumulada": [round(v, 4) for v in cumulative.tolist()],
        "loadings": loadings.to_dict(),
        "amostra_componentes": sample.to_dict(orient="records")
    }

@router.get("/association")
def association(
    min_support: float = 0.1,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    df["qual_alta"] = (df["overall_qual"] >= 7).astype(int)
    df["area_grande"] = (df["gr_liv_area"] >= df["gr_liv_area"].median()).astype(int)
    df["preco_alto"] = (df["sale_price"] >= df["sale_price"].median()).astype(int)
    df["garage_grande"] = (df["garage_area"] >= df["garage_area"].median()).astype(int)
    df["casa_nova"] = (df["year_built"] >= 1990).astype(int)
    rules = []
    binary_cols = ["qual_alta", "area_grande", "garage_grande", "casa_nova"]
    for col in binary_cols:
        support = df[col].mean()
        if support >= min_support:
            conf = df[df[col] == 1]["preco_alto"].mean()
            lift = conf / df["preco_alto"].mean()
            rules.append({
                "antecedente": col,
                "consequente": "preco_alto",
                "suporte": round(support, 4),
                "confianca": round(conf, 4),
                "lift": round(lift, 4)
            })
    rules.sort(key=lambda x: x["lift"], reverse=True)
    return {
        "usuario": current_user,
        "min_support": min_support,
        "regras": rules
    }