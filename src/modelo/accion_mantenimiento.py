from sqlalchemy.orm import backref
from sqlalchemy import Column, Integer, String, ForeignKey, REAL
from sqlalchemy.orm import relationship
from .declarative_base import Base
from src.modelo.mantenimiento import Mantenimiento


class AccionMantenimiento(Base):
    __tablename__ = 'accion_mantenimiento'

    id = Column(Integer, primary_key=True)
    costo = Column(REAL, nullable=False)
    fecha = Column(String, nullable=False)
    kilometraje = Column(Integer, nullable=False)

    vehiculoId = Column(Integer, ForeignKey('vehiculo.id'), nullable=False)
    vehiculo = relationship("Vehiculo", back_populates="accionMantenimiento")

    mantenimientoId = Column(Integer, ForeignKey('mantenimiento.id'), nullable=False)
    mantenimiento = relationship(Mantenimiento, backref=backref("accion_mantenimiento", uselist=False))
