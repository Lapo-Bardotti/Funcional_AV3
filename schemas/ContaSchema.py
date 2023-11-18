from pydantic import BaseModel


class ContaBase(BaseModel):
    ...


class ContaInsertRequest(ContaBase):
    tipo: str
    valor: float
    descricao: str


class ContaUpdateRequest(ContaBase):
    id: int
    tipo: str
    valor: float
    descricao: str


class ContaDeleteRequest(ContaBase):
    id: int


class ContaResponse(ContaBase):
    id: int
    tipo: str
    valor: float
    descricao: str

    class Config:
        from_attributes = True
