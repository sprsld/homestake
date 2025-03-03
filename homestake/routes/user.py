import json

from fastapi import APIRouter, Response, status

import homestake.constants as const
import homestake.encryption as encryption
from homestake.database.client import DatabaseClient, DatabaseClientError, DatabaseDuplicationError
from homestake.models import User, UserUpdate

DB_CLIENT = DatabaseClient()
user_router = APIRouter(
    tags=[const.API_TAG_USER]
)


@user_router.post('/users')
def create_user(request_body: User) -> Response:
    user_data = {
        "user_name": request_body.user_name,
        "email": request_body.email,
        "password": encryption.encrypt_password(request_body.password.get_secret_value()),
        "stake": request_body.stake
    }

    if request_body.lender:
        mortgage = DB_CLIENT.get_mortgage_by_lender(
            request_body.lender)
        if mortgage is not None:
            user_data["mortgage_id"] = mortgage["id"]

    if request_body.property_name:
        property = DB_CLIENT.get_property_by_name(request_body.property_name)
        if property is not None:
            user_data["property_id"] = property["id"]

    try:
        # def create_user(self, user_name: str, email: str, password: str, stake: int, mortgage_id: int = None, property_id: int = None)
        user = DB_CLIENT.create_user(**user_data)
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
        content=json.dumps(user),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@user_router.get('/users/{id}')
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


@user_router.get('/users/name/{user_name}')
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


@user_router.patch('/users/{id}')
def update_user(id: int, request_body: UserUpdate) -> Response:
    user = DB_CLIENT.get_user_by_id(id)
    if user is None:
        return Response(
            content=f"User with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    user_data = {k: v for k,
                 v in request_body.model_dump().items() if v is not None and k != "lender" and k != "property_name"}

    mortgage = DB_CLIENT.get_mortgage_by_lender(request_body.lender)
    if mortgage is None:
        return Response(
            content=f"Mortgage with lender {request_body.lender} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    else:
        user_data["mortgage_id"] = mortgage["id"]

    property = DB_CLIENT.get_property_by_name(request_body.property_name)
    if property is None:
        return Response(
            content=f"Property with name {request_body.property_name} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )
    else:
        user_data["property_id"] = property["id"]

    user = DB_CLIENT.update_user(id, **user_data)

    return Response(
        content=json.dumps(user),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )


@user_router.delete('/users/{id}')
def delete_user(id: int) -> Response:
    if DB_CLIENT.get_user_by_id(id) is None:
        return Response(
            content=f"User with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    DB_CLIENT.delete_user(id)

    return Response(
        content=None,
        status_code=status.HTTP_204_NO_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )
