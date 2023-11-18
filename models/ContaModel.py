from datetime import date
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from db import Base


class ContaModel(Base):
    __tablename__ = "contas"

    id: int = Column(Integer, primary_key=True, index=True)
    tipo: str = Column(String(1), nullable=False)
    valor: float = Column(Float, nullable=False)
    descricao: str = Column(Text, nullable=False)
    data_conta: date = Column(TIMESTAMP(timezone=True), nullable=False)
    criado_em = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))

    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("UsuarioModel")
