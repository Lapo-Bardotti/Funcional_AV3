from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from db import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    cpf: str = Column(String(14), nullable=False)
    senha: str = Column(Text, nullable=False)
    valor: float = Column(Float, nullable=False)
    foto: str = Column(Text, nullable=False)
    contas = relationship("ContaModel", back_populates="usuario")
