import json
import logging

from fastapi import APIRouter, Response, status

import homestake.constants as const
from homestake.database.client import DatabaseClient, DatabaseClientError, DatabaseDuplicationError
from homestake.models import Property, PropertyUpdate

DB_CLIENT = DatabaseClient()
property_router = APIRouter(
    tags=[const.API_TAG_PROPERTY]
)


@property_router.post('/properties')
def create_property(request_body: Property) -> Response:
    try:
        property = DB_CLIENT.create_property(request_body.name, request_body.address,
                                             request_body.purchase_price, request_body.purchase_date, request_body.current_value)
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
        content=json.dumps(property),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@property_router.get('/properties/address/{address}')
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


@property_router.get('/properties/{id}')
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


@property_router.get('/properties/name/{property_name}')
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


@property_router.patch('/properties/{id}')
def update_property(id: int, request_body: PropertyUpdate) -> Response:
    property = DB_CLIENT.get_property_by_id(id)
    if property is None:
        return Response(
            content=f"Property with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    property_data = {k: v for k,
                     v in request_body.model_dump().items() if v is not None}

    property = DB_CLIENT.update_property(id, **property_data)

    return Response(
        content=json.dumps(property),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )


@property_router.delete('/properties/{id}')
def delete_property(id: int) -> Response:
    if DB_CLIENT.get_property_by_id(id) is None:
        return Response(
            content=f"Property with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None
        )

    DB_CLIENT.delete_property(id)

    return Response(
        content=None,
        status_code=status.HTTP_204_NO_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )
