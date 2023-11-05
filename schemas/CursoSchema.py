from pydantic import BaseModel

class CursoBase(BaseModel):
    titulo: str
    descricao: str

class CursoRequest(CursoBase):
    ...

class CursoResponse(CursoBase):
    id: int

    class Config:
        from_attributes = True
