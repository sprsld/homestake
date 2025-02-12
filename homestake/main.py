from fastapi import FastAPI, Response, status
import json

from homestake.database.client import DatabaseClient

from homestake.models import Mortgage, Property, Transaction, User

app = FastAPI(
    title="HomeStake",
)

DB_CLIENT = DatabaseClient()


@app.get("/")
def read_root():
    return Response(
        content="Welcome to the HomeStake Equity and Contribution Tracker",
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get("/health")
def health():
    return Response(
        content="OK",
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.post("/mortgages")
def create_mortgage(request_body: Mortgage) -> Response:
    mortgage_data = {
        "lender": request_body.lender,
        "loan_amount": request_body.loan_amount,
        "interest_rate": request_body.interest_rate,
        "term": request_body.term,
        "start_date": request_body.start_date
    }

    if request_body.property_name:
        property = DB_CLIENT.get_property_by_name(request_body.property_name)
        if property is not None:
            mortgage_data["property_id"] = property["id"]

    mortgage = DB_CLIENT.create_mortgage(**mortgage_data)

    return Response(
        content=json.dumps(mortgage),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/mortgages/{id}')
def get_mortgage_by_id(id: int) -> Response:
    mortgage = DB_CLIENT.get_mortgage_by_id(id)
    if mortgage is None:
        return Response(
            content=f"Mortgage with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(mortgage),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/mortgages/lender/{lender}')
def get_mortgage_by_lender(lender: str) -> Response:
    mortgage = DB_CLIENT.get_mortgage_by_lender(lender)
    if mortgage is None:
        return Response(
            content=f"Mortgage with lender {lender} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(mortgage),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/mortgages/property/{property_name}')
def get_mortgage_by_property(property_name: str) -> Response:
    property = DB_CLIENT.get_property_by_name(property_name)
    if property is None:
        return Response(
            content=f"Property with name {property_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    mortgage = DB_CLIENT.get_mortgage_by_property(property["id"])
    if mortgage is None:
        return Response(
            content=f"Mortgage with property {property_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(mortgage),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.post('/properties')
def create_property(request_body: Property) -> Response:
    # name: str, address: str, purchase_price: float, purchase_date: datetime, current_value: float) -> Property:
    property = DB_CLIENT.create_property(request_body.name, request_body.address,
                                         request_body.purchase_price, request_body.purchase_date, request_body.current_value)

    return Response(
        content=json.dumps(property),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/properties/address/{address}')
def get_property_by_address(address: str) -> Response:
    property = DB_CLIENT.get_property_by_address(address)
    if property is None:
        return Response(
            content=f"Property with address {address} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(property),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/properties/{id}')
def get_property_by_id(id: int) -> Response:
    property = DB_CLIENT.get_property_by_id(id)
    if property is None:
        return Response(
            content=f"Property with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(property),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/properties/name/{property_name}')
def get_property_by_name(property_name: str) -> Response:
    property = DB_CLIENT.get_property_by_name(property_name)
    if property is None:
        return Response(
            content=f"Property with name {property_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(property),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.post('/transactions')
def create_transaction(request_body: Transaction) -> Response:
    transaction_data = {
        "amount": request_body.amount,
        "date": request_body.date
    }

    if request_body.user_name:
        user = DB_CLIENT.get_user_by_name(request_body.user_name)
        if user is not None:
            transaction_data["user_id"] = user["id"]

    if request_body.account_name:
        account = DB_CLIENT.get_account_by_name(request_body.account_name)

        if account is not None:
            transaction_data["account_id"] = account["id"]

    transaction = DB_CLIENT.create_transaction(**transaction_data)

    return Response(
        content=json.dumps(transaction),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/transactions/{id}')
def get_transaction_by_id(id: int) -> Response:
    transaction = DB_CLIENT.get_transaction_by_id(id)
    if transaction is None:
        return Response(
            content=f"Transaction with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(transaction),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/transactions/user/{user_name}')
def get_transaction_by_user(user_name: str) -> Response:
    user = DB_CLIENT.get_user_by_name(user_name)
    if user is None:
        return Response(
            content=f"User with name {user_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    transaction = DB_CLIENT.list_transactions_by_user(user["id"])
    if transaction is None:
        return Response(
            content=f"Transaction with user {user_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(transaction),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/transactions/account/{account_name}')
def get_transactions_by_account(account_name: str) -> Response:
    account = DB_CLIENT.get_account_by_name(account_name)
    if account is None:
        return Response(
            content=f"Account with name {account_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    transaction = DB_CLIENT.list_transactions_by_account(account["id"])
    if transaction is None:
        return Response(
            content=f"Transaction with account {account_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(transaction),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.post('/users')
def create_user(request_body: User) -> Response:
    user_data = {
        "user_name": request_body.user_name,
        "email": request_body.email,
        "stake": request_body.stake
    }

    if request_body.mortgage_lender:
        mortgage = DB_CLIENT.get_mortgage_by_lender(
            request_body.mortgage_lender)
        if mortgage is not None:
            user_data["mortgage_id"] = mortgage["id"]

    if request_body.property_name:
        property = DB_CLIENT.get_property_by_name(request_body.property_name)
        if property is not None:
            user_data["property_id"] = property["id"]

    user = DB_CLIENT.create_user(**user_data)

    return Response(
        content=json.dumps(user),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/users/{id}')
def get_user_by_id(id: int) -> Response:
    user = DB_CLIENT.get_user_by_id(id)
    if user is None:
        return Response(
            content=f"User with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(user),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )


@app.get('/users/name/{user_name}')
def get_user_by_name(user_name: str) -> Response:
    user = DB_CLIENT.get_user_by_name(user_name)
    if user is None:
        return Response(
            content=f"User with name {user_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    return Response(
        content=json.dumps(user),
        status_code=status.HTTP_200_OK,
        headers=None,
        media_type=None,
        background=None,
    )
