from pydantic import BaseModel


class UsuarioBase(BaseModel):
    ...


class UsuarioAuthRequest(UsuarioBase):
    cpf: str
    senha: str


class UsuarioInsertRequest(UsuarioBase):
    nome: str
    cpf: str
    senha: str
    saldo_conta: float


class UsuarioUpdateRequest(UsuarioBase):
    id: int
    nome: str
    cpf: str
    senha: str
    saldo_conta: float


class UsuarioDeleteRequest(UsuarioBase):
    id: int


class UsuarioResponse(UsuarioBase):
    id: int
    nome: str
    cpf: str
    saldo_conta: float

    class Config:
        from_attributes = True
