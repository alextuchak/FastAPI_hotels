from motor import motor_asyncio
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Any, Callable
from pydantic_core import core_schema
from app.settings import settings


client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
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


class PyPoint(BaseModel):
    type: str = Field(default="Point")
    coordinates: list = Field(...)

    @field_validator("type")
    def type_validate(cls, value):
        if value != "Point":
            raise ValueError("type must be Point")
        return value

    @field_validator("coordinates")
    def coords_validate(cls, value):
        if type(value) != list:
            raise ValueError("coordinates must be list")
        if not -180.0 < value[0] < 180.0:
            raise ValueError("coordinates must be list of longitude and latitude in range -180 - +180 and -90 - "
                             "+90 degrees")
        if not -90.0 < value[0] < 90.0:
            raise ValueError("coordinates must be list of longitude and latitude in range -180 - +180 and -90 - "
                             "+90 degrees")
        return value


PydanticObjectId = Annotated[
    ObjectId, PyObjectId
]


