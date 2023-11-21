from sqlalchemy.orm import Session

from models.ContaModel import ContaModel


class ContaRepository:
    @staticmethod
    def find_all(db: Session) -> list[ContaModel]:
        return db.query(ContaModel).all()

    @staticmethod
    def find_all_by_user(db: Session, id: int) -> list[ContaModel]:
        return db.query(ContaModel).filter(ContaModel.usuario_id == id)

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
    def find_all_by_user_date(db: Session, conta: ContaModel) -> list[ContaModel]:
        if conta.data_conta is None:
            return db.query(ContaModel).filter(ContaModel.usuario_id == conta.usuario_id).all()
        else:
            return db.query(ContaModel).filter(and_(
                ContaModel.usuario_id == conta.usuario_id,
                ContaModel.data_conta <= conta.data_conta
            )).all()

    @staticmethod
    def consultarSaldo(db: Session, conta: ContaModel) -> float:
        saldo_usuario = db.query(UsuarioModel.saldo_conta).filter(
            UsuarioModel.id == conta.usuario_id).scalar()

        if conta.data_conta is None:
            return saldo_usuario
        else:
            somatorio_contas_pagar = db.query(func.coalesce(func.sum(ContaModel.valor), 0)).filter(
                and_(and_(ContaModel.usuario_id == conta.usuario_id, ContaModel.tipo == 'p'),
                     ContaModel.data_conta <= conta.data_conta)).scalar()

            somatorio_contas_receber = db.query(func.coalesce(func.sum(ContaModel.valor), 0)).filter(
                and_(and_(ContaModel.usuario_id == conta.usuario_id, ContaModel.tipo == 'r'),
                     ContaModel.data_conta <= conta.data_conta)).scalar()

            return saldo_usuario - somatorio_contas_pagar + somatorio_contas_receber
