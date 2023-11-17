from pydantic import BaseModel, Field, field_validator, FileUrl, AnyUrl
from app.database import PyObjectId, PyPoint
from bson import ObjectId
from .schemas import Serv, Location
from fastapi import Query
from typing import Optional


class Hotel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(max_length=256)
    # room_types: list[Serv] = []
    rooms_quantity: int = Field(ge=1)
    stars: int = Field(ge=1, le=5)
    location: Location = Field(...)
    services: Optional[list[str]] = Query(None)
    coordinates: PyPoint = Field()

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Plaza",
                "room_types": [{"has_spa": True, "has_bar": True, "has_pool": False}],
                "rooms_quantity": 5,
                "stars": 4,
                "location": {
                    "country": "Brasil",
                    "city": "Brasil",
                    "zip": 123456,
                    "street": "Some street",
                    "building": "Some building",
                },
                "coordinates": {"coordinates": [75.5, 75.5]}
            }
        }


class ServiceTypes(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    logo_url: Optional[str] = Query(None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "_id": "6537ac8eff686ddb420d5448",
                "name": "service",
                "logo_url": "http://some.url.com",
            }
        }

# class Room(BaseModel):
#
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     hotel_name: str = Field(max_length=256)
#
#
#     @field_validator("hotel_name")
#     def validate_hotel_name(cls, value):
#         if not HotelsCRUD.get_hotels(value):
#             raise ValueError("hotel name must exist")
#         return value
