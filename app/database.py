from motor import motor_asyncio
from bson import ObjectId
from typing import Annotated, Any, Callable
from pydantic_core import core_schema

client = motor_asyncio.AsyncIOMotorClient('mongodb://root:example@localhost:27017')
db = client['hotels']


class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(input_value: str) -> ObjectId:
            return ObjectId(input_value)

        return core_schema.union_schema(
            [
                # check if it's an instance first before doing any further work
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.to_string_ser_schema(),
        )


PydanticObjectId = Annotated[
    ObjectId, PyObjectId
]

# async def session():
#     s = await client.start_session()
#     return s

# @app.on_event("startup")
# async def startup_event():
#     global client
#     global db
#     client = motor_asyncio.AsyncIOMotorClient('mongodb://root:example@mongo:2701')
#     db = client['hotels']
#     print(f"Connected to {db.name()}")
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     global client
#     client.close()
