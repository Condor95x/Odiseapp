from geoalchemy2 import Geometry
from database import Base
from sqlalchemy import Column, Integer, String, Float, Computed
class Parcela(Base):
    __tablename__ = "parcelas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    cultivo = Column(String, nullable=True)
    geom = Column(Geometry("POLYGON"), nullable=True)
    area = Column(Float, Computed("ST_Area(geom)", persisted=True))