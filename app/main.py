from fastapi import FastAPI
from .database import db
from app.hotels.router import router as hotels_routers
from app.settings import settings

app = FastAPI()

app.include_router(hotels_routers)


@app.get('/db')
async def asda():
    collection = db['hotels']
    return True
