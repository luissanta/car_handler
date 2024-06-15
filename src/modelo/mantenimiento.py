from sqlalchemy import Column, Integer, String
from .declarative_base import Base


class Mantenimiento(Base):
    __tablename__ = 'mantenimiento'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
