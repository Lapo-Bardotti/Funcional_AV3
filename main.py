import jwt
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn

from db import engine, Base, get_db
from models.UsuarioModel import UsuarioModel

from repositories.UsuarioRepository import UsuarioRepository
from schemas.UsuarioSchema import UsuarioAuthRequest, UsuarioInsertRequest, UsuarioUpdateRequest, UsuarioDeleteRequest, UsuarioResponse
from schemas.AuthRequest import AuthRequest

# extrair para .env, não seria exatamente necessário neste caso.
SECRET_KEY = 'sua_chave_secreta'

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def modify_request_response_middleware(request: Request, call_next):
    token = request.headers.get('Authorization')

    if request.headers.get('Req-Autenticar'):
        return await call_next(request)

    if token is None:
        response = JSONResponse(
            content={"detail": "Token inexistente"}, status_code=401)
    else:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            response = await call_next(request)
        except jwt.ExpiredSignatureError:
            response = JSONResponse(
                content={"detail": "Token expirado"}, status_code=401)
        except jwt.InvalidTokenError:
            response = JSONResponse(
                content={"detail": "Token inválido"}, status_code=401)

    return response


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
    usuario = UsuarioRepository.insert(
        db, UsuarioModel(**request.model_dump()))
    return UsuarioResponse.model_validate(usuario)


@app.post("/usuarios/editarUsuario/", status_code=status.HTTP_201_CREATED)
def editarUsuario(request: UsuarioUpdateRequest, db: Session = Depends(get_db)):
    usuario = UsuarioRepository.update(
        db, UsuarioModel(**request.model_dump()))
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
        "exp": datetime.utcnow() + timedelta(hours=0.5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
    # Lambda para criar o token


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
