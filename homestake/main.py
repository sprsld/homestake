from fastapi import FastAPI, Response, status

from homestake.routes.mortgage import mortgage_router
from homestake.routes.property import property_router
from homestake.routes.transaction import transaction_router
from homestake.routes.user import user_router

URL_PREFIX = "/api/v1"

app = FastAPI(
    title="HomeStake",
)


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


app.include_router(mortgage_router, prefix=URL_PREFIX)
app.include_router(property_router, prefix=URL_PREFIX)
app.include_router(transaction_router, prefix=URL_PREFIX)
app.include_router(user_router, prefix=URL_PREFIX)
