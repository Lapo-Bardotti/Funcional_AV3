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
    valor: float
    foto: str


class UsuarioUpdateRequest(UsuarioBase):
    id: int
    nome: str
    cpf: str
    senha: str
    valor: float
    foto: str

class UsuarioDeleteRequest(UsuarioBase):
    id: int

class UsuarioResponse(UsuarioBase):
    id: int
    nome: str
    cpf: str
    valor: float
    foto: str

    class Config:
        from_attributes = True
