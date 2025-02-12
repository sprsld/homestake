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


class Property(BaseModel):
    name: str
    address: str
    purchase_price: float
    purchase_date: datetime
    current_value: float

    model_config = ConfigDict(orm_mode=True)


class Transaction(BaseModel):
    amount: float
    date: datetime
    user_name: str
    account_name: str

    model_config = ConfigDict(orm_mode=True)


class User(BaseModel):
    user_name: str
    email: str
    stake: int
    mortgage_lender: Optional[str] = None
    property_name: Optional[str] = None

    @field_validator('stake')
    def validate_stake(cls, value):
        if value < 0 or value >= 100:
            raise ValueError('Stake must be between 0 and 100')
        return value

    model_config = ConfigDict(orm_mode=True)
