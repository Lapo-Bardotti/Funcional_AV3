from sqlalchemy.orm import Session

from models.UsuarioModel import UsuarioModel


class UsuarioRepository:
    @staticmethod
    def find_all(db: Session) -> list[UsuarioModel]:
        return db.query(UsuarioModel).all()

    @staticmethod
    def insert(db: Session, usuario: UsuarioModel) -> UsuarioModel:
        db.add(usuario)
        db.commit()
        return usuario

    @staticmethod
    def update(db: Session, usuario: UsuarioModel) -> UsuarioModel:
        db.merge(usuario)
        db.commit()
        return usuario

    @staticmethod
    def find_by_id(db: Session, id: int) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(UsuarioModel).filter(UsuarioModel.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        usuario = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        if usuario is not None:
            db.delete(usuario)
            db.commit()

    @staticmethod
    def find_by_cpf(db: Session, cpf: str) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.cpf == cpf).first()
