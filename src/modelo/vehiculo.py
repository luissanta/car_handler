from sqlalchemy import Column, Integer, String, REAL, Boolean
from sqlalchemy.orm import relationship
from .declarative_base import Base
from src.modelo.accion_mantenimiento import AccionMantenimiento


class Vehiculo(Base):
    __tablename__ = 'vehiculo'

    id = Column(Integer, primary_key=True)
    cilindraje = Column(REAL, nullable=False)
    color = Column(String, nullable=False)
    estado = Column(Boolean, nullable=False)
    kilometrajeCompra = Column(Integer, nullable=False)
    kilometrajeVenta = Column(Integer, nullable=True)
    marca = Column(String, nullable=False)
    modelo = Column(Integer, nullable=False)
    placa = Column(String, nullable=False)
    precioVenta = Column(REAL, nullable=True)
    tipoCombustible = Column(String, nullable=False)

    accionMantenimiento = relationship(AccionMantenimiento,
                                       back_populates="vehiculo",
                                       cascade='all, delete, delete-orphan')
