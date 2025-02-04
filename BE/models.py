from sqlalchemy import Column, Integer, String, Float, Computed
from geoalchemy2 import Geometry
from database import Base

class Parcela(Base):
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    geom = Column(Geometry("POLYGON"), nullable=True)
    cultivo = Column(String(50), nullable=True)
    area = Column(Float, Computed("ST_Area(geom)", persisted=True))