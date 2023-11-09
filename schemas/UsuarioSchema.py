from pydantic import BaseModel

class UsuarioBase(BaseModel):
    cpf: str
    senha: str

class UsuarioRequest(UsuarioBase):
    ...

class UsuarioResponse(UsuarioBase):
    nome: str
    cpf: str
    valor: float
    foto: str

    class Config:
        from_attributes = True
