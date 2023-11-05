from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from models.CursoModel import CursoModel
from db import engine, Base, get_db
from repositories.CursoRepository import CursoRepository
from schemas.CursoSchema import CursoRequest, CursoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def create(request: CursoRequest, db: Session = Depends(get_db)):
    curso = CursoRepository.save(db, CursoModel(**request.model_dump()))
    return CursoResponse.from_orm(curso)

@app.get("/api/cursos", response_model=list[CursoResponse])
def find_all(db: Session = Depends(get_db)):
    cursos = CursoRepository.find_all(db)
    return [CursoResponse.from_orm(curso) for curso in cursos]

# @app.get("/consultarSaldo")
# def consultarSaldo():
#     return {}

# @app.get("/cadastrarConta")
# def cadastrarConta():
#     return {}

# @app.get("/editarConta")
# def editarConta():
#     return {}

# @app.get("/deletarConta")
# def deletarConta():
#     return {}