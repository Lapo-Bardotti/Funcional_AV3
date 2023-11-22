from datetime import date
from pydantic import BaseModel


class ContaBase(BaseModel):
    ...


class ContasListAllRequest(ContaBase):
    usuario_id: int
    data_usuario: date = None

class ContaInsertRequest(ContaBase):
    tipo: str
    valor: float
    descricao: str
    data_conta: date
    usuario_id: int


class ContaUpdateRequest(ContaBase):
    id: int
    tipo: str
    valor: float
    descricao: str
    data_conta: date
    usuario_id: int


class ContaDeleteRequest(ContaBase):
    id: int


class ContaResponse(ContaBase):
    id: int
    tipo: str
    valor: float
    descricao: str
    data_conta: date
    usuario_id: int

    class Config:
        from_attributes = True
