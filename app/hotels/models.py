from pydantic import BaseModel, Field, field_validator
from app.database import PyObjectId, client, Any
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi import Body
from pymongo import ReadPreference
import bson


class Serv(BaseModel):
    serv: str = Field(...)
    option: str = Field(...)


class Hotel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(max_length=256)
    serv: list[Serv] = []
    location: str = Field(max_length=128)
    rooms_quantity: int = Field(ge=1)
    stars: int = Field(ge=1, le=5)

    @field_validator("serv")
    def validate_services(cls, value):
        print(value)
        return value

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Plaza",
                "location": "San Jose",
                "services": [{"has_spa": True, "has_bar": True, "has_pool": False}],
                "room_quantity": 5,
                "stars": 4
            }
        }


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
