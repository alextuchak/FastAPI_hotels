from app.hotels.models import Hotel, ServiceTypes
from app.base_crud import BaseCRUD
from motor import motor_asyncio


class HotelsCRUD(BaseCRUD):
    client = motor_asyncio.AsyncIOMotorClient("mongodb://root:example@localhost:27017")
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
    client = motor_asyncio.AsyncIOMotorClient("mongodb://root:example@localhost:27017")
    db = client['Hotels']
    collection = db.get_collection('service_types')
    served_model = ServiceTypes

    @classmethod
    async def get(cls, service_name) -> ServiceTypes:
        result = await cls.collection.find_one({"name": service_name})
        return result
