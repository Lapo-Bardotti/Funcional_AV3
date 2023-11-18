from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.UsuarioModel import UsuarioModel

class ContaModel(Base):
    __tablename__ = "contas"

    id: int = Column(Integer, primary_key=True, index=True)
    tipo: str = Column(String(1), nullable=False)  # "p" para contas a pagar, "r" para contas a receber
    valor: float = Column(Float, nullable=False)
    descricao: str = Column(Text, nullable=False)

    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario: UsuarioModel = relationship("UsuarioModel", back_populates="contas")
