from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class Mortgage(BaseModel):
    lender: str
    loan_amount: float
    interest_rate: int
    term: int
    start_date: datetime
    property_name: Optional[str] = None

    model_config = ConfigDict(orm_mode=True)


class MortgageUpdate(Mortgage):
    lender: Optional[str] | None = None
    loan_amount: Optional[float] | None = None
    interest_rate: Optional[int] | None = None
    term: Optional[int] | None = None
    start_date: Optional[datetime] | None = None
    property_name: Optional[str] | None = None

    model_config = ConfigDict(orm_mode=True)


class Property(BaseModel):
    name: str
    address: str
    purchase_price: float
    purchase_date: datetime
    current_value: float

    model_config = ConfigDict(orm_mode=True)


class PropertyUpdate(Property):
    name: Optional[str] | None = None
    address: Optional[str] | None = None
    purchase_price: Optional[float] | None = None
    purchase_date: Optional[datetime] | None = None
    current_value: Optional[float] | None = None

    model_config = ConfigDict(orm_mode=True)


class Transaction(BaseModel):
    amount: float
    date: datetime
    user_name: str
    account_name: str

    model_config = ConfigDict(orm_mode=True)


class TransactionUpdate(Transaction):
    amount: Optional[float] | None = None
    date: Optional[datetime] | None = None
    user_name: Optional[str] | None = None
    account_name: Optional[str] | None = None

    model_config = ConfigDict(orm_mode=True)


class User(BaseModel):
    user_name: str
    email: str
    stake: int
    lender: Optional[str] = None
    property_name: Optional[str] = None

    @field_validator('stake')
    def validate_stake(cls, value):
        if value < 0 or value >= 100:
            raise ValueError('Stake must be between 0 and 100')
        return value

    model_config = ConfigDict(orm_mode=True)


class UserUpdate(User):
    user_name: Optional[str] | None = None
    email: Optional[str] | None = None
    stake: Optional[int] | None = None
    lender: Optional[str] | None = None
    property_name: Optional[str] | None = None

    @field_validator('stake')
    def validate_stake(cls, value):
        if value < 0 or value >= 100:
            raise ValueError('Stake must be between 0 and 100')
        return value

    model_config = ConfigDict(orm_mode=True)
