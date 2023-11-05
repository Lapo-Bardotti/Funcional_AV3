from sqlalchemy.orm import Session

from models.CursoModel import CursoModel

class CursoRepository:
    @staticmethod
    def find_all(db: Session) -> list[CursoModel]:
        return db.query(CursoModel).all()

    @staticmethod
    def save(db: Session, curso: CursoModel) -> CursoModel:
        if curso.id:
            db.merge(curso)
        else:
            db.add(curso)
        db.commit()
        return curso

    @staticmethod
    def find_by_id(db: Session, id: int) -> CursoModel:
        return db.query(CursoModel).filter(CursoModel.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(CursoModel).filter(CursoModel.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        curso = db.query(CursoModel).filter(CursoModel.id == id).first()
        if curso is not None:
            db.delete(curso)
            db.commit()
