import json

from fastapi import APIRouter, Response, status

import homestake.constants as const
from homestake.database.client import DatabaseClient, DatabaseClientError, DatabaseDuplicationError
from homestake.models import Mortgage, MortgageUpdate

DB_CLIENT = DatabaseClient()
mortgage_router = APIRouter(
    tags=[const.API_TAG_MORTGAGE]
)


@mortgage_router.post("/mortgages")
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

    try:
        mortgage = DB_CLIENT.create_mortgage(**mortgage_data)
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
        content=json.dumps(mortgage),
        status_code=status.HTTP_201_CREATED,
        headers=None,
        media_type=None,
        background=None,
    )


@mortgage_router.get('/mortgages/{id}')
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


@mortgage_router.get('/mortgages/lender/{lender}')
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


@mortgage_router.get('/mortgages/property/{property_name}')
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


@mortgage_router.patch('/mortgages/{id}')
def update_mortgage(id: int, request_body: MortgageUpdate) -> Response:
    mortgage = DB_CLIENT.get_mortgage_by_id(id)
    if mortgage is None:
        return Response(
            content=f"Mortgage with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    mortgage_data = {k: v for k,
                     v in request_body.model_dump().items() if v is not None and k != "property_name"}

    if request_body.property_name:
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
            mortgage_data["property_id"] = property["id"]

    mortgage = DB_CLIENT.update_mortgage(id, **mortgage_data)

    return Response(
        content=json.dumps(mortgage),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )


@mortgage_router.delete('/mortgages/{id}')
def delete_mortgage(id: int) -> Response:
    if DB_CLIENT.get_mortgage_by_id(id) is None:
        return Response(
            content=f"Mortgage with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            headers=None,
            media_type=None,
            background=None,
        )

    DB_CLIENT.delete_mortgage(id)

    return Response(
        content=None,
        status_code=status.HTTP_204_NO_CONTENT,
        headers=None,
        media_type=None,
        background=None,
    )
