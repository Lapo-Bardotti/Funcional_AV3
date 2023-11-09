from sqlalchemy.orm import Session

from models.UsuarioModel import UsuarioModel


class UsuarioRepository:
    @staticmethod
    def find_all(db: Session) -> list[UsuarioModel]:
        return db.query(UsuarioModel).all()

    @staticmethod
    def save(db: Session, curso: UsuarioModel) -> UsuarioModel:
        if curso.id:
            db.merge(curso)
        else:
            db.add(curso)
        db.commit()
        return curso

    @staticmethod
    def find_by_id(db: Session, id: int) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(UsuarioModel).filter(UsuarioModel.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        curso = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        if curso is not None:
            db.delete(curso)
            db.commit()

    @staticmethod
    def find_by_cpf(db: Session, cpf: str) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.cpf == cpf).first()
