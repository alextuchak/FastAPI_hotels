from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, APIRouter, Body, status, Depends
from .dependecies import HotelsSearchArgs
from .models import Hotel
from .service import HotelsCRUD

router = APIRouter(
    prefix='/hotels',
)


@router.post(
    '/test_db',
    response_model=Hotel,
    status_code=status.HTTP_201_CREATED,
    description="New hotel creation",
)
async def test_create(hotel: Hotel = Body(...)):
    response = await HotelsCRUD.create(hotel)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


@router.get(
    '/get_hotels',
    response_model=list[Hotel],
    status_code=status.HTTP_200_OK,
    description='Get all hotels'
)
async def get_hotels(search_args: HotelsSearchArgs = Depends()
                     ):
    response = await HotelsCRUD.get_hotels(search_args)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)
