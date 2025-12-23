from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProyectoLey(Base):
    __tablename__ = 'proyectos_ley'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(Text)
    fecha_radicacion = Column(DateTime)
    resumen = Column(Text)
    enlace = Column(String)
    estado = Column(String)
    pais = Column(String)
    sector_economico = Column(String)