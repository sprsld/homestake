from __future__ import annotations
from typing import List, Optional

from datetime import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

import homestake.constants as constants

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'
    __mapper_args__ = {
        "polymorphic_identity": "account",
        "polymorphic_on": "type",
    }
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(constants.NAME_LENGTH), unique=True, index=True)
    type: Mapped[str] = mapped_column(String(constants.NAME_LENGTH))

    transactions: Mapped[Optional[List["Transaction"]]] = relationship()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        }


class Mortgage(Account):
    __tablename__ = 'mortgages'
    __mapper_args__ = {
        'polymorphic_identity': 'mortgage'
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), primary_key=True)
    lender: Mapped[str] = mapped_column(
        String(constants.NAME_LENGTH), index=True)
    loan_amount: Mapped[float]
    interest_rate: Mapped[int]
    term: Mapped[int]
    start_date: Mapped[datetime]
    property_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('properties.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'mortgage'

    def __repr__(self) -> str:
        return f"Mortgage(id={self.id}, lender={self.lender}, loan_amount={self.loan_amount}, interest_rate={self.interest_rate}, term={self.term}, start_date={self.start_date}, property_id={self.property_id})"

    def to_dict(self):
        model_dict = {
            'id': self.id,
            'name': self.name,
            'lender': self.lender,
            'loan_amount': self.loan_amount,
            'interest_rate': self.interest_rate,
            'term': self.term,
            'start_date': self.start_date.isoformat()
        }

        return model_dict


class Property(Base):
    __tablename__ = 'properties'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(constants.NAME_LENGTH), unique=True, index=True)
    address: Mapped[str] = mapped_column(
        String(constants.ADDR_LENGTH), unique=True, index=True)
    purchase_price: Mapped[float]
    purchase_date: Mapped[datetime]
    current_value: Mapped[float]

    mortgage: Mapped[Optional["Mortgage"]] = relationship()
    users: Mapped[Optional[List["User"]]] = relationship()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat(),
            'current_value': self.current_value
        }


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float]
    date: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    account_id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date.isoformat(),
            'user_id': self.user_id,
            'account_id': self.account_id
        }


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(
        String(constants.NAME_LENGTH), unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(String(constants.PASS_MAX_LENGTH))
    stake: Mapped[Optional[int]]
    property_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('properties.id'))
    mortgage_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('mortgages.id'))

    transactions: Mapped[List["Transaction"]] = relationship()

    def to_dict(self):
        model_dict = {
            'id': self.id,
            'user_name': self.user_name,
            'email': self.email,
            'stake': self.stake
        }

        if self.mortgage_id:
            model_dict['mortgage_id'] = self.mortgage_id
        if self.property_id:
            model_dict['property_id'] = self.property_id

        return model_dict
