from app.database import client
from fastapi.encoders import jsonable_encoder
from fastapi import Body
from bson.objectid import ObjectId


class BaseCRUD:
    """
    Base class for CRUD operation.
    """

    client = client
    db = None
    collection = None
    served_model = None

    @classmethod
    async def create(cls, input_data: served_model = Body(...)) -> served_model:
        input_data = jsonable_encoder(input_data)
        new_db_record = await cls.collection.insert_one(input_data)
        created_data = await cls.collection.find_one({"_id": new_db_record.inserted_id})
        return created_data

    @classmethod
    async def get_one(cls, id: str) -> served_model:
        result = await cls.collection.find_one({"_id": id})
        return result

    @classmethod
    async def delete_one(cls, id: str):
        data = await cls.get_one(id)
        if data:
            await cls.collection.delete_one({"_id": id})
            return True
        return False

    @classmethod
    async def update_one(cls, id: str, update: dict) -> served_model or bool:
        if not isinstance(update, dict):
            return False
        data = await cls.get_one(id)
        if data:
            await cls.collection.update_one({"_id": id},
                                            {"$set": update})
            updated_data = await cls.get_one(id)
            return updated_data
        return False



