from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import get_current_user
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

router = APIRouter()

def get_dataframe(db: Session):
    houses = db.query(models.House).all()
    df = pd.DataFrame([{
        "lot_area": h.lot_area, "overall_qual": h.overall_qual,
        "overall_cond": h.overall_cond, "year_built": h.year_built,
        "gr_liv_area": h.gr_liv_area, "full_bath": h.full_bath,
        "half_bath": h.half_bath, "bedroom_abvgr": h.bedroom_abvgr,
        "totrms_abvgrd": h.totrms_abvgrd, "garage_cars": h.garage_cars,
        "garage_area": h.garage_area, "sale_price": h.sale_price
    } for h in houses]).dropna()
    df["price_category"] = (df["sale_price"] >= df["sale_price"].median()).astype(int)
    return df

@router.get("/knn")
def knn_classification(
    k: int = 5,
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
    y = df["price_category"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred).tolist()
    return {
        "usuario": current_user,
        "modelo": "KNN",
        "k": k,
        "metricas": {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "f1_score": round(f1_score(y_test, y_pred), 4)
        },
        "matriz_confusao": cm
    }

@router.get("/random-forest")
def random_forest_classification(
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
    y = df["price_category"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred).tolist()
    importances = dict(zip(features, [round(i, 4) for i in model.feature_importances_]))
    return {
        "usuario": current_user,
        "modelo": "Random Forest",
        "metricas": {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "f1_score": round(f1_score(y_test, y_pred), 4)
        },
        "matriz_confusao": cm,
        "importancia_features": importances
    }