import jwt
from datetime import datetime, timedelta
from cpf import verificarCPF

from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn

from db import engine, Base, get_db
from models.UsuarioModel import UsuarioModel
from models.ContaModel import ContaModel

from repositories.UsuarioRepository import UsuarioRepository
from schemas.UsuarioSchema import UsuarioAuthRequest, UsuarioInsertRequest, UsuarioUpdateRequest, UsuarioDeleteRequest, UsuarioResponse

from repositories.ContaRepository import ContaRepository
from schemas.ContaSchema import ContasListAllRequest, ContaInsertRequest, ContaUpdateRequest, ContaDeleteRequest, ContaResponse


# extrair para .env, não seria exatamente necessário neste caso.
SECRET_KEY = 'sua_chave_secreta'

Base.metadata.create_all(bind=engine)
cpf_valido = lambda cpf: verificarCPF(cpf)

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
                content={"detail": "Token expirado"}, status_code=403)
        except jwt.InvalidTokenError:
            response = JSONResponse(
                content={"detail": "Token inválido"}, status_code=403)

    return response


@app.post("/usuarios/autenticar/", status_code=status.HTTP_200_OK)
def autenticar(request: UsuarioAuthRequest, db: Session = Depends(get_db)):
    find_by_cpf = lambda db: lambda req: UsuarioRepository.find_by_cpf(db, req.cpf) # currying
    usuario = find_by_cpf(db)(request) # currying
    if usuario and usuario.senha == request.senha:
        usuarioResponse = UsuarioResponse.model_validate(usuario)
        response_data = {
            "usuario": usuarioResponse,
            "token": create_jwt_token(usuario.id)
        }
        return response_data if usuarioResponse else None # if ternário
    return "Usuário ou senha inválido."

    # Lambda que verifica se tem usuario e retorna a response_data

@app.post("/usuarios/cadastrarUsuario/", status_code=status.HTTP_201_CREATED)
def cadastrarUsuario(request: UsuarioInsertRequest, db: Session = Depends(get_db)):
    insert = lambda db: lambda fn: UsuarioRepository.insert(db, fn(**request.model_dump())) # HOF (high order function)
    return UsuarioResponse.model_validate(insert(db)(UsuarioModel)) if cpf_valido(request.cpf) else "Objeto inválido."


@app.patch("/usuarios/editarUsuario/", status_code=status.HTTP_201_CREATED)
def editarUsuario(request: UsuarioUpdateRequest, db: Session = Depends(get_db)):

    usuario = UsuarioRepository.update(
        db, UsuarioModel(**request.model_dump()))
    return UsuarioResponse.model_validate(usuario)


@app.delete("/usuarios/deletarUsuario/", status_code=status.HTTP_202_ACCEPTED)
def deletarUsuario(request: UsuarioDeleteRequest, db: Session = Depends(get_db)):

    usuario = UsuarioRepository.exists_by_id(db, request.id)
    if usuario:
        UsuarioRepository.delete_by_id(db, request.id)
        return "usuario deletado."
    else:
        return "usuario nao encontrado."
    # Extrair if else em lambdas


@app.post("/contas/cadastrarConta/", status_code=status.HTTP_201_CREATED)
def cadastrarConta(request: ContaInsertRequest, db: Session = Depends(get_db)):

    conta = ContaRepository.insert(
        db, ContaModel(**request.model_dump()))
    return ContaResponse.model_validate(conta)


@app.post("/contas/listarContas/", status_code=status.HTTP_201_CREATED)
def listarContas(request: ContasListAllRequest, db: Session = Depends(get_db)):

    contas = ContaRepository.find_all_by_user(db, request.usuario_id)
    contas_validadas = [ContaResponse.model_validate(
        conta) for conta in contas]
    return contas_validadas


@app.patch("/contas/editarConta/", status_code=status.HTTP_201_CREATED)
def editarConta(request: ContaUpdateRequest, db: Session = Depends(get_db)):

    conta = ContaRepository.update(
        db, ContaModel(**request.model_dump()))
    return ContaResponse.model_validate(conta)


@app.delete("/contas/deletarConta/", status_code=status.HTTP_202_ACCEPTED)
def deletarConta(request: ContaDeleteRequest, db: Session = Depends(get_db)):

    conta = ContaRepository.exists_by_id(db, request.id)
    if conta:
        ContaRepository.delete_by_id(db, request.id)
        return "conta deletada."
    else:
        return "conta nao encontrado."


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
