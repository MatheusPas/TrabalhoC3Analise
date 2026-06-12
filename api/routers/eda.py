from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/missing-values")
def missing_values(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    total = db.query(func.count(models.House.id)).scalar()
    fields = [
        "ms_zoning", "lot_area", "street", "neighborhood",
        "overall_qual", "overall_cond", "year_built", "year_remod_add",
        "gr_liv_area", "full_bath", "half_bath", "bedroom_abvgr",
        "kitchen_abvgr", "totrms_abvgrd", "garage_cars", "garage_area",
        "sale_price"
    ]
    result = {}
    for field in fields:
        col = getattr(models.House, field)
        nulls = db.query(func.count()).filter(col == None).scalar()
        result[field] = {
            "missing": nulls,
            "missing_pct": round((nulls / total) * 100, 2)
        }
    return {"usuario": current_user, "total_registros": total, "missing_values": result}

@router.get("/correlations")
def correlations(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    houses = db.query(models.House).all()
    numeric_fields = [
        "lot_area", "overall_qual", "overall_cond", "year_built",
        "year_remod_add", "gr_liv_area", "full_bath", "half_bath",
        "bedroom_abvgr", "totrms_abvgrd", "garage_cars", "garage_area",
        "sale_price"
    ]
    import pandas as pd
    data = [{f: getattr(h, f) for f in numeric_fields} for h in houses]
    df = pd.DataFrame(data)
    corr = df.corr()["sale_price"].sort_values(ascending=False).round(4)
    return {
        "usuario": current_user,
        "correlacao_com_preco": corr.to_dict()
    }

@router.get("/distribution")
def distribution(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    stats = db.query(
        func.min(models.House.sale_price).label("min"),
        func.max(models.House.sale_price).label("max"),
        func.avg(models.House.sale_price).label("media"),
        func.percentile_cont(0.25).within_group(models.House.sale_price).label("q1"),
        func.percentile_cont(0.50).within_group(models.House.sale_price).label("mediana"),
        func.percentile_cont(0.75).within_group(models.House.sale_price).label("q3")
    ).first()
    return {
        "usuario": current_user,
        "distribuicao_preco": {
            "min": stats.min,
            "max": stats.max,
            "media": round(stats.media, 2),
            "q1": stats.q1,
            "mediana": stats.mediana,
            "q3": stats.q3
        }
    }