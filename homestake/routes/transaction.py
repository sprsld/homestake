import json

from fastapi import APIRouter, Response, status

import homestake.constants as constants
from homestake.database.client import DatabaseClient, DatabaseClientError, DatabaseDuplicationError
from homestake.models import Transaction, TransactionUpdate

DB_CLIENT = DatabaseClient()
transaction_router = APIRouter(
    tags=[constants.API_TAG_TRANSACTION]
)


@transaction_router.post('/transactions')
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

    try:
        transaction = DB_CLIENT.create_transaction(**transaction_data)
    except DatabaseDuplicationError as e:
        return Response(
            content=str(e),
            status_code=status.HTTP_409_CONFLICT,
            headers=None,
            media_type=None,
            background=None,
        )
    except DatabaseClientError as e:
        return Response(
            content=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=None,
            media_type=None,
            background=None,
        )

    return Response(
        content=json.dumps(transaction),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@transaction_router.get('/transactions/{id}')
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


@transaction_router.get('/transactions/user/{user_name}')
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


@transaction_router.get('/transactions/account/{account_name}')
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


@transaction_router.patch('/transactions/{id}')
def update_transaction(id: int, request_body: TransactionUpdate) -> Response:
    transaction = DB_CLIENT.get_transaction_by_id(id)
    if transaction is None:
        return Response(
            content=f"Transaction with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    transaction_data = {k: v for k,
                        v in request_body.model_dump().items() if v is not None and k != "user_name" and k != "account_name"}

    if request_body.user_name:
        user = DB_CLIENT.get_user_by_name(request_body.user_name)
        if user is None:
            return Response(
                content=f"User with name {request_body.user_name} not found",
                status_code=status.HTTP_404_NOT_FOUND,
                headers=None,
                media_type=None,
                background=None,
            )
        else:
            transaction_data["user_id"] = user["id"]

    if request_body.account_name:
        account = DB_CLIENT.get_account_by_name(request_body.account_name)
        if account is None:
            return Response(
                content=f"Account with name {request_body.account_name} not found",
                status_code=status.HTTP_404_NOT_FOUND,
                headers=None,
                media_type=None,
                background=None,
            )
        else:
            transaction_data["account_id"] = account["id"]

    transaction = DB_CLIENT.update_transaction(id, **transaction_data)

    return Response(
        content=json.dumps(transaction),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )


@transaction_router.delete('/transactions/{id}')
def delete_transaction(id: int) -> Response:
    if DB_CLIENT.get_transaction_by_id(id) is None:
        return Response(
            content=f"Transaction with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    DB_CLIENT.delete_transaction(id)

    return Response(
        content=None,
        status_code=status.HTTP_204_NO_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )
