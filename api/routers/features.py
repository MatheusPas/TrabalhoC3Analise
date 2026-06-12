from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import get_current_user
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder

router = APIRouter()

def get_dataframe(db: Session):
    houses = db.query(models.House).all()
    return pd.DataFrame([{
        "id": h.id, "ms_subclass": h.ms_subclass, "ms_zoning": h.ms_zoning,
        "lot_area": h.lot_area, "street": h.street, "neighborhood": h.neighborhood,
        "overall_qual": h.overall_qual, "overall_cond": h.overall_cond,
        "year_built": h.year_built, "year_remod_add": h.year_remod_add,
        "gr_liv_area": h.gr_liv_area, "full_bath": h.full_bath,
        "half_bath": h.half_bath, "bedroom_abvgr": h.bedroom_abvgr,
        "kitchen_abvgr": h.kitchen_abvgr, "totrms_abvgrd": h.totrms_abvgrd,
        "garage_cars": h.garage_cars, "garage_area": h.garage_area,
        "sale_price": h.sale_price
    } for h in houses])

@router.get("/new-features")
def new_features(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    df["house_age"] = 2024 - df["year_built"]
    df["remod_age"] = 2024 - df["year_remod_add"]
    df["total_bath"] = df["full_bath"] + (0.5 * df["half_bath"])
    df["area_per_room"] = df["gr_liv_area"] / df["totrms_abvgrd"].replace(0, 1)
    sample = df[["id", "house_age", "remod_age", "total_bath", "area_per_room", "sale_price"]].head(10)
    return {
        "usuario": current_user,
        "novas_features": sample.to_dict(orient="records")
    }

@router.get("/normalize")
def normalize(
    method: str = "minmax",
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    numeric = ["lot_area", "gr_liv_area", "garage_area", "sale_price"]
    scaler = MinMaxScaler() if method == "minmax" else StandardScaler()
    scaled = scaler.fit_transform(df[numeric])
    df_scaled = pd.DataFrame(scaled, columns=numeric)
    return {
        "usuario": current_user,
        "metodo": method,
        "amostra_normalizada": df_scaled.head(10).round(4).to_dict(orient="records")
    }

@router.get("/encode")
def encode(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    categorical = ["ms_zoning", "street", "neighborhood"]
    le = LabelEncoder()
    encoded = {}
    for col in categorical:
        df[col + "_encoded"] = le.fit_transform(df[col].astype(str))
        encoded[col] = dict(zip(le.classes_.tolist(), le.transform(le.classes_).tolist()))
    sample = df[["id"] + [c + "_encoded" for c in categorical]].head(10)
    return {
        "usuario": current_user,
        "mapeamento": encoded,
        "amostra_encoded": sample.to_dict(orient="records")
    }