from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class Mortgage(BaseModel):
    lender: str
    loan_amount: float
    interest_rate: int
    term: int
    start_date: datetime
    property_name: str | None = None

    model_config = ConfigDict(orm_mode=True)


class MortgageUpdate(Mortgage):
    lender: str | None = None
    loan_amount: float | None = None
    interest_rate: int | None = None
    term: int | None = None
    start_date: datetime | None = None
    property_name: str | None = None

    model_config = ConfigDict(orm_mode=True)


class Property(BaseModel):
    name: str
    address: str
    purchase_price: float
    purchase_date: datetime
    current_value: float

    model_config = ConfigDict(orm_mode=True)


class PropertyUpdate(Property):
    name: str | None = None
    address: str | None = None
    purchase_price: float | None = None
    purchase_date: datetime | None = None
    current_value: float | None = None

    model_config = ConfigDict(orm_mode=True)


class Transaction(BaseModel):
    amount: float
    date: datetime
    user_name: str
    account_name: str

    model_config = ConfigDict(orm_mode=True)


class TransactionUpdate(Transaction):
    amount: float | None = None
    date: datetime | None = None
    user_name: str | None = None
    account_name: str | None = None

    model_config = ConfigDict(orm_mode=True)


class User(BaseModel):
    user_name: str
    email: str
    stake: int
    lender: str | None = None
    property_name: str | None = None

    @field_validator('stake')
    def validate_stake(cls, value):
        if value < 0 or value >= 100:
            raise ValueError('Stake must be between 0 and 100')
        return value

    model_config = ConfigDict(orm_mode=True)


class UserUpdate(User):
    user_name: str | None = None
    email: str | None = None
    stake: int | None = None
    lender: str | None = None
    property_name: str | None = None

    @field_validator('stake')
    def validate_stake(cls, value):
        if value < 0 or value >= 100:
            raise ValueError('Stake must be between 0 and 100')
        return value

    model_config = ConfigDict(orm_mode=True)
