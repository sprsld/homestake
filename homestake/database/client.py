import os
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from typing import List

import homestake.constants as const
from homestake.database.models import Base, Account, Mortgage, Property, Transaction, User
from homestake.logger import logger


class DatabaseClientError(Exception):
    """Custom exception for DatabaseClient errors."""
    pass


class DatabaseDuplicationError(DatabaseClientError):
    """Custom exception for DatabaseClient duplication errors."""
    pass


class DatabaseClient:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        if database_url is None:
            self.engine = create_engine("sqlite:///./homestake.db")
        else:
            self.engine = create_engine(database_url)

        Base.metadata.create_all(self.engine)

    ### Account ###
    def list_accounts(self) -> List[Account]:
        with Session(self.engine) as session:
            accounts = session.query(Account).all()
            return [account.to_dict() for account in accounts]

    def get_account_by_name(self, name: str) -> Account:
        with Session(self.engine) as session:
            account = session.query(Account).filter_by(name=name).first()
            return account.to_dict() if account else None

    ### Mortgage ###
    def create_mortgage(self, lender: str, loan_amount: float, interest_rate: int, term: int, start_date: datetime, name="Mortgage", property_id: int = None) -> Mortgage:
        with Session(self.engine) as session:
            mortgage = Mortgage(
                lender=lender,
                name=name,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                term=term,
                start_date=start_date.replace(tzinfo=timezone.utc),
                property_id=property_id
            )

            try:
                session.add(mortgage)
                session.commit()
            except IntegrityError as e:
                logger.info(e)
                session.rollback()
                # SQLITE_DB_ENTRY_EXISTS_MSG in str(e) accounts for local db
                if const.DB_ENTRY_EXISTS_MSG in str(e) or const.SQLITE_DB_ENTRY_EXISTS_MSG in str(e):
                    raise DatabaseDuplicationError(
                        const.MORTGAGE_EXISTS_MSG) from e
                else:
                    raise DatabaseClientError(
                        const.MORTGAGE_CREATE_ERROR_MSG) from e
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.MORTGAGE_CREATE_ERROR_MSG) from e

            return mortgage.to_dict()

    def get_mortgage_by_id(self, mortgage_id: int) -> Mortgage:
        with Session(self.engine) as session:
            mortgage = session.query(Mortgage).filter_by(
                id=mortgage_id).first()
            return mortgage.to_dict() if mortgage else None

    def get_mortgage_by_lender(self, lender: str) -> Mortgage:
        with Session(self.engine) as session:
            mortgage = session.query(Mortgage).filter_by(
                lender=lender).first()
            return mortgage.to_dict() if mortgage else None

    def get_mortgage_by_property(self, property_id: int) -> Mortgage:
        with Session(self.engine) as session:
            mortgage = session.query(Mortgage).filter_by(
                property_id=property_id).first()
            return mortgage.to_dict() if mortgage else None

    def update_mortgage(self, mortgage_id: int, **kwargs) -> Mortgage:
        with Session(self.engine) as session:
            mortgage = session.query(Mortgage).filter_by(
                id=mortgage_id).first()
            if not mortgage:
                raise DatabaseClientError(
                    const.MORTGAGE_ID_NOT_FOUND.format(mortgage_id))

            for key, value in kwargs.items():
                if hasattr(mortgage, key):
                    setattr(mortgage, key, value)
                else:
                    raise DatabaseClientError(
                        const.MORTGAGE_INVALID_ATTR_MSG.format(key))

            try:
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.MORTGAGE_UPDATE_ERROR_MSG) from e

            return mortgage.to_dict()

    def delete_mortgage(self, mortgage_id: int):
        with Session(self.engine) as session:
            mortgage = session.query(Mortgage).filter_by(
                id=mortgage_id).first()
            if not mortgage:
                raise DatabaseClientError(
                    const.MORTGAGE_ID_NOT_FOUND.format(mortgage_id))

            try:
                session.delete(mortgage)
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.MORTGAGE_DELETE_ERROR_MSG) from e

            return mortgage.to_dict()

    def list_mortgages(self) -> List[Mortgage]:
        with Session(self.engine) as session:
            mortgages = session.query(Mortgage).all()
            return [mortgage.to_dict() for mortgage in mortgages]

    ### Property ###

    def create_property(self, name: str, address: str, purchase_price: float, purchase_date: datetime, current_value: float) -> Property:
        with Session(self.engine) as session:
            property = Property(
                name=name,
                address=address,
                purchase_price=purchase_price,
                purchase_date=purchase_date.replace(tzinfo=timezone.utc),
                current_value=current_value
            )

            try:
                session.add(property)
                session.commit()
            except IntegrityError as e:
                logger.info(e)
                session.rollback()
                # SQLITE_DB_ENTRY_EXISTS_MSG in str(e) accounts for local db
                if const.DB_ENTRY_EXISTS_MSG in str(e) or const.SQLITE_DB_ENTRY_EXISTS_MSG in str(e):
                    raise DatabaseDuplicationError(
                        const.PROPERTY_EXISTS_MSG) from e
                else:
                    raise DatabaseClientError(
                        const.PROPERTY_CREATE_ERROR_MSG) from e

            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.PROPERTY_CREATE_ERROR_MSG) from e

            return property.to_dict()

    def get_property_by_address(self, address: str) -> Property:
        with Session(self.engine) as session:
            property = session.query(Property).filter_by(
                address=address).first()
            return property.to_dict() if property else None

    def get_property_by_id(self, property_id: int) -> Property:
        with Session(self.engine) as session:
            property = session.query(Property).filter_by(
                id=property_id).first()
            return property.to_dict() if property else None

    def get_property_by_name(self, name: str) -> Property:
        with Session(self.engine) as session:
            property = session.query(Property).filter_by(
                name=name).first()
            return property.to_dict() if property else None

    def update_property(self, property_id: int, **kwargs) -> Property:
        with Session(self.engine) as session:
            property = session.query(Property).filter_by(
                id=property_id).first()
            if not property:
                raise DatabaseClientError(
                    const.PROPERTY_ID_NOT_FOUND.format(property_id))

            for key, value in kwargs.items():
                if hasattr(property, key):
                    setattr(property, key, value)
                else:
                    raise DatabaseClientError(
                        const.PROPERTY_INVALID_ATTR_MSG.format(key))

            try:
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.PROPERTY_UPDATE_ERROR_MSG) from e

            return property.to_dict()

    def delete_property(self, property_id: int):
        with Session(self.engine) as session:
            property = session.query(Property).filter_by(
                id=property_id).first()
            if not property:
                raise DatabaseClientError(
                    const.PROPERTY_ID_NOT_FOUND.format(property_id))

            try:
                session.delete(property)
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.PROPERTY_DELETE_ERROR_MSG) from e

            return property.to_dict()

    ### Transaction ###

    def create_transaction(self, amount: float, date: datetime, user_id: int, account_id: int) -> Transaction:
        with Session(self.engine) as session:
            transaction = Transaction(
                amount=amount,
                user_id=user_id,
                date=date,
                account_id=account_id
            )

            try:
                session.add(transaction)
                session.commit()
            except IntegrityError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.TRANSACTION_CREATE_ERROR_MSG) from e
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.TRANSACTION_CREATE_ERROR_MSG) from e
            return transaction.to_dict()

    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        with Session(self.engine) as session:
            transaction = session.query(
                Transaction).filter_by(id=transaction_id).first()
            return transaction.to_dict() if transaction else None

    def list_transactions_by_user(self, user_id: int) -> List[Transaction]:
        with Session(self.engine) as session:
            transactions = session.query(
                Transaction).filter_by(user_id=user_id).all()
            return [transaction.to_dict() for transaction in transactions]

    def list_transactions_by_account(self, account_id: int) -> List[Transaction]:
        with Session(self.engine) as session:
            account = session.query(Account).filter_by(id=account_id).first()
            if not account:
                raise DatabaseClientError(
                    const.ACCOUNT_ID_NOT_FOUND.format(account_id))
            return [transaction.to_dict() for transaction in account.transactions]

    def update_transaction(self, transaction_id: int, **kwargs) -> Transaction:
        with Session(self.engine) as session:
            transaction = session.query(
                Transaction).filter_by(id=transaction_id).first()
            if not transaction:
                raise DatabaseClientError(
                    const.TRANSACTION_ID_NOT_FOUND.format(transaction_id))

            for key, value in kwargs.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)
                else:
                    raise DatabaseClientError(
                        const.TRANSACTION_INVALID_ATTR_MSG.format(key))

            try:
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.TRANSACTION_UPDATE_ERROR_MSG) from e

            return transaction.to_dict()

    def delete_transaction(self, transaction_id: int):
        with Session(self.engine) as session:
            transaction = session.query(
                Transaction).filter_by(id=transaction_id).first()
            if not transaction:
                raise DatabaseClientError(
                    const.TRANSACTION_ID_NOT_FOUND.format(transaction_id))

            try:
                session.delete(transaction)
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.TRANSACTION_DELETE_ERROR_MSG) from e

            return transaction.to_dict()

    def list_transactions(self) -> List[Transaction]:
        with Session(self.engine) as session:
            transactions = session.query(Transaction).all()
            return [transaction.to_dict() for transaction in transactions]

    ### User ###

    def create_user(self, user_name: str, email: str, stake: int, mortgage_id: int = None, property_id: int = None) -> User:
        with Session(self.engine) as session:
            user = User(
                user_name=user_name,
                email=email,
                stake=stake,
                mortgage_id=mortgage_id,
                property_id=property_id
            )

            try:
                session.add(user)
                session.commit()
            except IntegrityError as e:
                logger.info(e)
                session.rollback()
                # SQLITE_DB_ENTRY_EXISTS_MSG in str(e) accounts for local db
                if const.DB_ENTRY_EXISTS_MSG in str(e) or const.SQLITE_DB_ENTRY_EXISTS_MSG in str(e):
                    raise DatabaseDuplicationError(
                        const.USER_EXISTS_MSG) from e
                else:
                    raise DatabaseClientError(
                        const.USER_CREATE_ERROR_MSG) from e
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.USER_CREATE_ERROR_MSG) from e

            return user.to_dict()

    def get_user_by_name(self, user_name: str) -> User:
        with Session(self.engine) as session:
            user = session.query(User).filter_by(user_name=user_name).first()
            return user.to_dict() if user else None

    def get_user_by_id(self, user_id: int) -> User:
        with Session(self.engine) as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user.to_dict() if user else None

    def update_user(self, user_id: int, **kwargs) -> User:
        with Session(self.engine) as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise DatabaseClientError(
                    const.USER_ID_NOT_FOUND.format(user_id))

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise DatabaseClientError(
                        const.USER_INVALID_ATTR_MSG.format(key))

            try:
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.USER_UPDATE_ERROR_MSG) from e

            return user.to_dict()

    def delete_user(self, user_id: int):
        with Session(self.engine) as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise DatabaseClientError(
                    const.USER_ID_NOT_FOUND.format(user_id))

            try:
                session.delete(user)
                session.commit()
            except SQLAlchemyError as e:
                logger.info(e)
                session.rollback()
                raise DatabaseClientError(
                    const.USER_DELETE_ERROR_MSG) from e

            return user.to_dict()

    def list_users(self) -> List[User]:
        with Session(self.engine) as session:
            users = session.query(User).all()
            return [user.to_dict() for user in users]
