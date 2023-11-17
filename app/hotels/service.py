from app.database import client
from app.hotels.models import Hotel, ServiceTypes
from app.base_crud import BaseCRUD as CRUD
from fastapi.encoders import jsonable_encoder
from fastapi import Body


class BaseCRUD:
    client = client
    db = client['Hotels']
    collection = db.get_collection('hotels')


class HotelsCRUD(CRUD):
    db = client['Hotels']
    collection = db.get_collection('hotels')
    served_model = Hotel

    @classmethod
    async def get_hotels(cls, search_args) -> list[Hotel]:
        hotels = []
        async for hotel in cls.collection.find().skip(search_args.offset).limit(search_args.limit):
            hotels.append(hotel)
        return hotels

    @classmethod
    async def delete_one(cls, id: str):
        # TO-DO find all related to hotel info and delete it also
        if await super().delete_one(id):
            return True
        return False





class ServiceTypeCRUD(BaseCRUD):
    db = client['Hotels']
    collection = db.get_collection('service_types')

    @classmethod
    async def create(cls, service_types: ServiceTypes = Body(...)) -> list[ServiceTypes]:
        service_type = jsonable_encoder(service_types)
        new_service = await cls.collection.insert_one(service_type)
        created_service = await cls.collection.find_one({"_id": new_service.inserted_id})
        return created_service

    @classmethod
    async def get(cls, service_name) -> ServiceTypes:
        result = await cls.collection.find_one({"name": service_name})
        return result
