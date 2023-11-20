from operator import and_
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from models.ContaModel import ContaModel
from models.UsuarioModel import UsuarioModel


class ContaRepository:
    @staticmethod
    def find_all(db: Session) -> list[ContaModel]:
        return db.query(ContaModel).all()

    @staticmethod
    def find_all_by_user_date(db: Session, conta: ContaModel) -> list[ContaModel]:
        if conta.data_conta is None:
            return db.query(ContaModel).filter(ContaModel.usuario_id == conta.usuario_id).all()
        else:
            return db.query(ContaModel).filter(and_(
                ContaModel.usuario_id == conta.usuario_id,
                ContaModel.data_conta <= conta.data_conta
            )).all()

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

    @staticmethod
    def consultarSaldo(db: Session, conta: ContaModel) -> float:
        saldo_usuario = db.query(UsuarioModel.saldo_conta).filter(
            UsuarioModel.id == conta.usuario_id).scalar()

        somatorio_contas = db.query(func.coalesce(func.sum(ContaModel.valor), 0)).filter(
            ContaModel.usuario_id == conta.usuario_id).scalar()

        diferenca = saldo_usuario - somatorio_contas

        return diferenca
