from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Text,Float,Computed
from sqlalchemy.orm import relationship, deferred
from geoalchemy2 import Geometry
from app.database.db import Base

# Modelo de la tabla 'parcelas'
class Parcela(Base):
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    geom = Column(Geometry("POLYGON", srid=4326), nullable=True)
    cultivo = Column(String(50), nullable=True)
    area = Column(Float, Computed("ST_Area(geom)", persisted=True))  # Calculado como campo generado

    # Relación con otras tablas
    analisis = relationship("Analisis", back_populates="parcela", cascade="all, delete")
    historico_rendimiento = relationship("HistoricoRendimiento", back_populates="parcela", cascade="all, delete")


# Modelo de la tabla 'clima'
class clima(Base):
    __tablename__ = "clima"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), nullable=True)
    fecha = Column(Date, nullable=False)
    temperatura = Column(Numeric, nullable=True)  # En grados Celsius
    precipitacion = Column(Numeric, nullable=True)  # En milímetros
    viento = Column(Numeric, nullable=True)  # En km/h


# Modelo de la tabla 'analisis'
class Analisis(Base):
    __tablename__ = "analisis"

    id = Column(Integer, primary_key=True, index=True)
    parcela_id = Column(Integer, ForeignKey("parcelas.id", ondelete="CASCADE"), nullable=False)
    fecha = Column(Date, nullable=False)
    nitrogeno = Column(Numeric, nullable=True)  # Contenido de N (kg/ha o ppm)
    fosforo = Column(Numeric, nullable=True)  # Contenido de P (kg/ha o ppm)
    potasio = Column(Numeric, nullable=True)  # Contenido de K (kg/ha o ppm)

    # Relación con la tabla 'parcelas'
    parcela = relationship("Parcela", back_populates="analisis")


# Modelo de la tabla 'historico_rendimiento'
class HistoricoRendimiento(Base):
    __tablename__ = "historico_rendimiento"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    parcela_id = Column(Integer, ForeignKey("parcelas.id", ondelete="CASCADE"), nullable=False)
    kilos = Column(Numeric, nullable=False)  # Rendimiento total en kilogramos
    calidad = Column(String(50), nullable=True)  # Ejemplo: "Alta", "Media", "Baja"
    comentario = Column(Text, nullable=True)  # Comentarios adicionales

    # Relación con la tabla 'parcelas'
    parcela = relationship("Parcela", back_populates="historico_rendimiento")