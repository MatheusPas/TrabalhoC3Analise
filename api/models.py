from sqlalchemy import Column, Integer, Float, String
from database import Base

class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    ms_subclass = Column(Integer)
    ms_zoning = Column(String)
    lot_area = Column(Integer)
    street = Column(String)
    neighborhood = Column(String)
    overall_qual = Column(Integer)
    overall_cond = Column(Integer)
    year_built = Column(Integer)
    year_remod_add = Column(Integer)
    gr_liv_area = Column(Integer)
    full_bath = Column(Integer)
    half_bath = Column(Integer)
    bedroom_abvgr = Column(Integer)
    kitchen_abvgr = Column(Integer)
    totrms_abvgrd = Column(Integer)
    garage_cars = Column(Float)
    garage_area = Column(Float)
    sale_price = Column(Integer)