from sqlalchemy.orm import Session

from models.ContaModel import ContaModel


class ContaRepository:
    @staticmethod
    def find_all(db: Session) -> list[ContaModel]:
        return db.query(ContaModel).all()

    @staticmethod
    def insert(db: Session, conta: ContaModel) -> ContaModel:
        db.add(conta)
        db.commit()
        return conta

    @staticmethod
    def update(db: Session, conta: ContaModel) -> ContaModel:
        db.merge(conta)
        db.commit()
        return conta

    @staticmethod
    def find_by_id(db: Session, id: int) -> ContaModel:
        return db.query(ContaModel).filter(ContaModel.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(ContaModel).filter(ContaModel.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        conta = db.query(ContaModel).filter(ContaModel.id == id).first()
        if conta is not None:
            db.delete(conta)
            db.commit()
