from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import get_current_user
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

router = APIRouter()

def get_dataframe(db: Session):
    houses = db.query(models.House).all()
    return pd.DataFrame([{
        "lot_area": h.lot_area, "overall_qual": h.overall_qual,
        "overall_cond": h.overall_cond, "year_built": h.year_built,
        "gr_liv_area": h.gr_liv_area, "full_bath": h.full_bath,
        "half_bath": h.half_bath, "bedroom_abvgr": h.bedroom_abvgr,
        "totrms_abvgrd": h.totrms_abvgrd, "garage_cars": h.garage_cars,
        "garage_area": h.garage_area, "sale_price": h.sale_price
    } for h in houses]).dropna()

@router.get("/simple")
def simple_regression(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    X = df[["gr_liv_area"]]
    y = df["sale_price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return {
        "usuario": current_user,
        "modelo": "Regressão Linear Simples",
        "variavel": "gr_liv_area",
        "coeficiente": round(model.coef_[0], 4),
        "intercepto": round(model.intercept_, 4),
        "metricas": {
            "RMSE": round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
            "MAE": round(mean_absolute_error(y_test, y_pred), 2),
            "R2": round(r2_score(y_test, y_pred), 4)
        }
    }

@router.get("/multiple")
def multiple_regression(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    df = get_dataframe(db)
    features = [
        "lot_area", "overall_qual", "overall_cond", "year_built",
        "gr_liv_area", "full_bath", "half_bath", "bedroom_abvgr",
        "totrms_abvgrd", "garage_cars", "garage_area"
    ]
    X = df[features]
    y = df["sale_price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    coefs = dict(zip(features, [round(c, 4) for c in model.coef_]))
    return {
        "usuario": current_user,
        "modelo": "Regressão Linear Múltipla",
        "coeficientes": coefs,
        "intercepto": round(model.intercept_, 4),
        "metricas": {
            "RMSE": round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
            "MAE": round(mean_absolute_error(y_test, y_pred), 2),
            "R2": round(r2_score(y_test, y_pred), 4)
        }
    }