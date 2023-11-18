from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from db import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    cpf: str = Column(String(14), nullable=False)
    senha: str = Column(Text, nullable=False)
    saldo_conta: float = Column(Float, nullable=False)
    criado_em = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text('now()'))
