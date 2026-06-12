from pydantic import BaseModel
from typing import Optional

class HouseBase(BaseModel):
    ms_subclass: Optional[int] = None
    ms_zoning: Optional[str] = None
    lot_area: Optional[int] = None
    street: Optional[str] = None
    neighborhood: Optional[str] = None
    overall_qual: Optional[int] = None
    overall_cond: Optional[int] = None
    year_built: Optional[int] = None
    year_remod_add: Optional[int] = None
    gr_liv_area: Optional[int] = None
    full_bath: Optional[int] = None
    half_bath: Optional[int] = None
    bedroom_abvgr: Optional[int] = None
    kitchen_abvgr: Optional[int] = None
    totrms_abvgrd: Optional[int] = None
    garage_cars: Optional[float] = None
    garage_area: Optional[float] = None
    sale_price: Optional[int] = None

class HouseResponse(HouseBase):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str