from pydantic import BaseModel, Field


class Serv(BaseModel):
    name: str = Field(...)
    option: str = Field(...)


class Location(BaseModel):
    country: str = Field(...)
    city: str = Field(...)
    zip: int = Field(...)
    street: str = Field(...)
    building: str = Field(...)
