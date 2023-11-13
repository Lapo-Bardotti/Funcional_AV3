import jwt
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from db import engine, Base, get_db
from models.UsuarioModel import UsuarioModel

from repositories.UsuarioRepository import UsuarioRepository
from schemas.UsuarioSchema import UsuarioAuthRequest, UsuarioInsertRequest, UsuarioUpdateRequest, UsuarioDeleteRequest, UsuarioResponse
from schemas.AuthRequest import AuthRequest

SECRET_KEY = 'sua_chave_secreta'  # extrair para .env, não seria exatamente necessário neste caso.

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/usuarios/autenticar/", status_code=status.HTTP_200_OK)
def autenticar(request: UsuarioAuthRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.find_by_cpf(db, request.cpf)
    usuarioResponse = UsuarioResponse.model_validate(usuario)
    if usuarioResponse:
        response_data = {
            "usuario": usuarioResponse,
            "token": create_jwt_token(usuario.id)
        }
        return response_data
    # Lambda que verifica se tem usuario e retorna a response_data


@app.post("/usuarios/cadastrarUsuario/", status_code=status.HTTP_201_CREATED)
def cadastrarUsuario(request: UsuarioInsertRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.insert(db, UsuarioModel(**request.model_dump()))
    return UsuarioResponse.model_validate(usuario)


@app.post("/usuarios/editarUsuario/", status_code=status.HTTP_201_CREATED)
def editarUsuario(request: UsuarioUpdateRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.update(db, UsuarioModel(**request.model_dump()))
    return UsuarioResponse.model_validate(usuario)


@app.post("/usuarios/deletarUsuario/", status_code=status.HTTP_202_ACCEPTED)
def deletarUsuario(request: UsuarioDeleteRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.exists_by_id(db, request.id)
    if usuario:
        UsuarioRepository.delete_by_id(db, request.id)
        return "usuario deletado."
    else:
        return "usuario nao encontrado."
    # Extrair if else em lambdas


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
