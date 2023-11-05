from app.database import client
from .models import Hotel
from fastapi.encoders import jsonable_encoder
from fastapi import Body


class HotelsCRUD:
    client = client
    db = client['Hotels']
    collection = db.get_collection('hotels')

    @classmethod
    async def create(cls, hotel: Hotel = Body(...)) -> list[Hotel]:
        hotel = jsonable_encoder(hotel)
        new_hotel = await cls.collection.insert_one(hotel)
        created_hotel = await cls.collection.find_one({"_id": new_hotel.inserted_id})
        return created_hotel

    @classmethod
    async def get_hotels(cls, search_args) -> list[Hotel]:
        hotels = []
        async for hotel in cls.collection.find().skip(search_args.offset).limit(search_args.limit):
            hotels.append(hotel)
        return hotels
