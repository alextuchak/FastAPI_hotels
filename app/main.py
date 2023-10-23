from fastapi import FastAPI, Query, APIRouter, Body, status, Depends
from typing import Optional
from .hotels.models import Hotel, HotelsCRUD
from .database import db
from fastapi.responses import JSONResponse

app = FastAPI()

router = APIRouter()


class HotelsSearchArgs:

    def __init__(
            self,
            location: str,
            stars: Optional[int] = Query(None, ge=1, le=5),
            limit: Optional[int] = Query(20, ge=1, le=100),
            offset: Optional[int] = Query(0, ge=0, )

    ):
        self.location = location
        self.stars = stars
        self.limit = limit
        self.offset = offset


@app.post('/test_db', response_model=Hotel)
async def test_create(hotel: Hotel = Body(...)):
    response = await HotelsCRUD.create(hotel)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)


@app.get('/get_hotels', response_model=list[Hotel])
async def get_hotels(search_args: HotelsSearchArgs = Depends()
                     ):
    response = await HotelsCRUD.get_hotels(search_args)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@app.get('/db')
async def asda():
    collection = db['hotels']
    return True
