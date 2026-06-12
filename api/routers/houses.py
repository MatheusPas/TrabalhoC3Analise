from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas
from database import get_db
from auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.HouseResponse])
def get_houses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return db.query(models.House).offset(skip).limit(limit).all()

@router.get("/stats/summary")
def get_stats(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    stats = db.query(
        func.count(models.House.id).label("total"),
        func.avg(models.House.sale_price).label("preco_medio"),
        func.min(models.House.sale_price).label("preco_minimo"),
        func.max(models.House.sale_price).label("preco_maximo"),
        func.avg(models.House.gr_liv_area).label("area_media"),
        func.avg(models.House.overall_qual).label("qualidade_media")
    ).first()
    return {
        "usuario": current_user,
        "total_casas": stats.total,
        "preco_medio": round(stats.preco_medio, 2) if stats.preco_medio else None,
        "preco_minimo": stats.preco_minimo,
        "preco_maximo": stats.preco_maximo,
        "area_media": round(stats.area_media, 2) if stats.area_media else None,
        "qualidade_media": round(stats.qualidade_media, 2) if stats.qualidade_media else None
    }

@router.get("/neighborhood/{neighborhood}", response_model=List[schemas.HouseResponse])
def get_by_neighborhood(
    neighborhood: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    houses = db.query(models.House).filter(
        models.House.neighborhood == neighborhood
    ).all()
    if not houses:
        raise HTTPException(status_code=404, detail="Bairro não encontrado")
    return houses

@router.get("/{house_id}", response_model=schemas.HouseResponse)
def get_house(
    house_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    house = db.query(models.House).filter(models.House.id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="Casa não encontrada")
    return house