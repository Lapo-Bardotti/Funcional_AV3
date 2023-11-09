import jwt
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from db import engine, Base, get_db

from repositories.UsuarioRepository import UsuarioRepository
from schemas.UsuarioSchema import UsuarioRequest, UsuarioResponse
from schemas.AuthRequest import AuthRequest

SECRET_KEY = 'sua_chave_secreta'  # extrair

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/usuarios/autenticar/", status_code=status.HTTP_200_OK)
def autenticar(request: UsuarioRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.find_by_cpf(db, request.cpf)
    usuarioResponse = UsuarioResponse.model_validate(usuario)
    if usuarioResponse:
        response_data = {
            "usuario": usuarioResponse,
            "token": create_jwt_token(usuario.id)
        }
        return response_data
    # Lambda que verifica se tem usuario e retorna a response_data


@app.post("/usuarios/testarToken")
def testarToken(request: AuthRequest):
    return jwt.decode(request.token, SECRET_KEY, algorithms=["HS256"])


def create_jwt_token(user_id):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token
    # Lambda para criar o token
